from dataclasses import dataclass
from functools import wraps
import os
from random import random
import tritonclient.http.aio as httpclient

import asyncio
import numpy as np
import aiofiles
import logging
import click
import json
import orjson

from time import perf_counter as timer
from typing import Dict, List, Optional, Tuple

from pydantic.error_wrappers import ValidationError

from mlserver.batching.requests import BatchedRequests
from mlserver.types import InferenceRequest, InferenceResponse, Parameters
from mlserver.codecs import NumpyCodec
from mlserver.logging import get_logger


from mlserver.utils import generate_uuid
from mlserver.batching.requests import _merge_parameters


CHOICES_TRANSPORT = ["rest", "grpc"]
FINALIZER_REPORT_FREQUENCY = 100
RETRY_SLEEP_TIME = 1

logger = get_logger()


# Monkey patching is required for error responses coming from MLServer.
# MLServer will contain `detail` field instead of `error` one like Triton.
async def _get_error(response):
    """
    Returns the InferenceServerException object if response
    indicates the error. If no error then return None
    """
    if response.status != 200:
        result = await response.read()
        error_response = json.loads(result) if len(result) else {"error": ""}
        try:
            return httpclient.InferenceServerException(msg=error_response["error"])
        except KeyError:
            return httpclient.InferenceServerException(
                msg=json.dumps(error_response["detail"])
            )
    else:
        return None


httpclient._get_error = _get_error
del _get_error


def click_async(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@dataclass
class BatchInputItem:
    index: int
    item: bytes


@dataclass
class BatchOutputItem:
    index: int
    item: bytes


def setup_logging(debug: bool):
    if debug:
        logger.setLevel(logging.DEBUG)


def get_headers(request_id: str, headers: Dict[str, str]) -> Dict[str, str]:
    headers = {"content-type": "application/json", **headers}
    if request_id:
        headers["seldon-puid"] = request_id
        headers["x-request-id"] = request_id
    return headers


@dataclass
class TritonRequest:
    id: str
    inputs: List[httpclient.InferInput]
    outputs: Optional[List[httpclient.InferRequestedOutput]]

    @classmethod
    def from_inference_request(
        cls, inference_request: InferenceRequest, binary_data: bool
    ) -> "TritonRequest":
        inputs = []
        for request_input in inference_request.inputs or []:
            new_input = httpclient.InferInput(
                request_input.name, request_input.shape, request_input.datatype
            )
            request_input_np = NumpyCodec.decode_input(request_input)

            # Change datatype if BYTES to satisfy Tritonclient checks
            if request_input.datatype == "BYTES":
                request_input_np = request_input_np.astype(np.object_)

            new_input.set_data_from_numpy(
                request_input_np,
                binary_data=binary_data,
            )
            inputs.append(new_input)
        outputs = []
        for request_output in inference_request.outputs or []:
            new_output = httpclient.InferRequestedOutput(
                request_output.name, binary_data=binary_data
            )
            outputs.append(new_output)

        if inference_request.id is None:
            request_id = ""
        else:
            request_id = inference_request.id
        return TritonRequest(request_id, inputs, outputs)


def infer_result_to_infer_response(item: httpclient.InferResult) -> InferenceResponse:
    infer_response = item.get_response()

    outputs = []
    for response_output in infer_response["outputs"]:
        name = response_output["name"]
        output = NumpyCodec.encode_output(name, item.as_numpy(name))

        # Drop "binary_data_size" from `paramaters` as we decoded the output
        parameters = response_output.get("parameters")
        if parameters is not None:
            # Create copy in case this code will ever be used in another context as
            # we are modifying the original parameters by removing unwanted key
            parameters = parameters.copy()
            if "binary_data_size" in parameters:
                del parameters["binary_data_size"]
            output.parameters = Parameters(**parameters)

        outputs.append(output)

    inference_response = InferenceResponse(
        model_name=infer_response["model_name"],
        model_version=infer_response.get("model_version", None),
        id=infer_response.get("id", None),
        parameters=infer_response.get("parameters", None),
        outputs=outputs,
    )

    return inference_response


def _preprocess_headers(headers: List[str]) -> Dict[str, str]:
    output = {}
    for item in headers:
        try:
            key, val = [x.strip() for x in item.split(":")]
            output[key] = val
        except ValueError:
            logger.error(f"Cannot process '{item}' as valid header. Ignoring.")
    return output


def _verify_write_access(fpath: str):
    return os.access(os.path.dirname(os.path.abspath(fpath)), os.W_OK)


def _serialize_validation_error(index: int, error: ValidationError) -> BatchOutputItem:
    msg = {
        "parameters": {"batch_index": index},
        "error": {"status": "preprocessing error", "msg": error.errors()},
    }
    return BatchOutputItem(item=json.dumps(msg).encode(), index=index)


def _serialize_inference_error(index: int, error: Exception) -> BatchOutputItem:
    msg = {
        "parameters": {"batch_index": index},
        "error": {"status": "preprocessing error", "msg": str(error)},
    }
    return BatchOutputItem(item=json.dumps(msg).encode(), index=index)


def preprocess_items(
    items: List[BatchInputItem], binary_data: bool
) -> Tuple[TritonRequest, BatchedRequests, List[BatchOutputItem], Dict[str, int]]:
    item_indices = {}
    inference_requests = {}
    invalid_inputs = []
    for item in items:
        try:
            inference_request = InferenceRequest.parse_obj(orjson.loads(item.item))
            # try to use `id` from the input file to identify each request in the batch
            if inference_request.id is None:
                inference_request.id = generate_uuid()
            inference_requests[inference_request.id] = inference_request
            item_indices[inference_request.id] = item.index
        except ValidationError as e:
            logger.error(
                f"preprocessing error: batch_index={item.index}, error={repr(e)}"
            )
            invalid_inputs.append(_serialize_validation_error(item.index, e))
    batched = BatchedRequests(inference_requests)
    # Set `id` for batched requests - if only single request use its own id
    if len(inference_requests) == 1:
        batched.merged_request.id = inference_request.id
    else:
        batched.merged_request.id = generate_uuid()
    return (
        TritonRequest.from_inference_request(batched.merged_request, binary_data),
        batched,
        invalid_inputs,
        item_indices,
    )


def postprocess_items(
    infer_result: httpclient.InferResult,
    batched: BatchedRequests,
    item_indices: Dict[str, int],
) -> List[BatchOutputItem]:
    full_inference_response = infer_result_to_infer_response(infer_result)
    output_items = []
    for item_id, inference_response in batched.split_response(
        full_inference_response
    ).items():
        # Add `id` used for batched requests to Parameters under `inference_id` key
        new_params = {
            "batch_index": item_indices[item_id],
            "inference_id": full_inference_response.id,
        }
        inference_response.parameters = Parameters(
            **_merge_parameters(new_params, inference_response)
        )

        output_items.append(
            BatchOutputItem(
                index=item_indices[item_id], item=inference_response.json().encode()
            )
        )
    return output_items


async def send_requests(
    model_name: str,
    triton_client: httpclient.InferenceServerClient,
    triton_request: TritonRequest,
    headers: Dict[str, str],
    retries: int,
    worker_id: int,
) -> httpclient.InferResult:
    for i in range(retries):
        try:
            return await triton_client.infer(
                model_name,
                triton_request.inputs,
                outputs=triton_request.outputs,
                request_id=triton_request.id,
                headers=get_headers(triton_request.id, headers),
            )
        except Exception as e:
            logger.error(
                f"consumer {worker_id}: retries {i+1}/{retries}, exception {e}"
            )
            if i + 1 == retries:
                raise
            await asyncio.sleep(RETRY_SLEEP_TIME)


async def process_items(
    items: List[BatchInputItem],
    model_name: str,
    worker_id: int,
    retries: int,
    triton_client: httpclient.InferenceServerClient,
    headers: Dict[str, str],
    binary_data: bool,
) -> List[BatchOutputItem]:
    try:
        triton_request, batched, invalid_inputs, inference_indices = preprocess_items(
            items, binary_data
        )
        if len(invalid_inputs) == len(items):
            return invalid_inputs
    except Exception as e:
        logger.error(f"consumer {worker_id}: failed to preprocess items: {e}")
        raise

    try:
        logger.debug(f"consumer {worker_id}: sending request")
        infer_result = await send_requests(
            model_name,
            triton_client,
            triton_request,
            headers,
            retries,
            worker_id,
        )
        logger.debug(f"consumer {worker_id}: received response")
    except Exception as e:
        logger.error(f"consumer {worker_id}: failed to process task: {e}")
        failed_results = [
            _serialize_inference_error(index, e) for index in inference_indices.values()
        ]
        return failed_results + invalid_inputs

    try:
        output_items = postprocess_items(infer_result, batched, inference_indices)
    except Exception as e:
        logger.error(f"consumer {worker_id}: failed to postprocess item: {e}")

    return output_items + invalid_inputs


async def produce(
    queue: "asyncio.Queue[List[BatchInputItem]]", fname: str, batch_size: int
):
    async with aiofiles.open(fname, "rb") as f:
        index = 0
        batch = []
        async for line in f:
            batch.append(BatchInputItem(index=index, item=line))
            if len(batch) == batch_size:
                await queue.put(batch)
                batch = []
            index += 1
        if batch:
            await queue.put(batch)


async def consume(
    model_name: str,
    worker_id: int,
    retries: int,
    batch_interval: float,
    batch_jitter: float,
    triton_client: httpclient.InferenceServerClient,
    headers: Dict[str, str],
    binary_data: bool,
    extra_verbose: bool,
    queue_in: "asyncio.Queue[List[BatchInputItem]]",
    queue_out: "asyncio.Queue[List[BatchOutputItem]]",
):
    while True:
        input_items = await queue_in.get()
        try:
            start_time = timer()
            output_items = await process_items(
                input_items,
                model_name,
                worker_id,
                retries,
                triton_client,
                headers,
                binary_data,
            )
            if batch_interval > 0 or batch_jitter > 0:
                total_sleep_time = batch_interval + random() * batch_jitter
                remaining_sleep_time = total_sleep_time - (timer() - start_time)
                logger.debug(
                    f"consume {worker_id}: sleeping for {remaining_sleep_time:.3f}"
                )
                await asyncio.sleep(remaining_sleep_time)
        except Exception:
            if extra_verbose:
                logger.error(
                    f"consumer {worker_id}: failed to process item {input_items}"
                )
            queue_in.task_done()
            continue

        await queue_out.put(output_items)
        queue_in.task_done()


async def finalize(queue: "asyncio.Queue[List[BatchOutputItem]]", fname: str) -> int:
    # TODO: Test if output directory is writtable, sysexit otherwise.
    counter = 0
    try:
        async with aiofiles.open(fname, "wb") as f:
            while True:
                batch_output = await queue.get()
                for item in batch_output:
                    try:
                        await f.write(item.item)
                        await f.write(b"\n")
                    except Exception as e:
                        logger.error(f"Failed to finalize task: {repr(e)}")
                    counter += 1
                    if counter % FINALIZER_REPORT_FREQUENCY == 0:
                        logger.info(f"Finalizer: processed instances: {counter}")
                queue.task_done()
    except asyncio.CancelledError:
        return counter


async def process_batch(
    model_name: str,
    url: str,
    workers: int,
    retries: int,
    batch_size: int,
    input_data_path: str,
    output_data_path: str,
    binary_data: bool,
    transport: str,
    request_headers: List[str],
    timeout: float,
    batch_interval: float,
    batch_jitter: float,
    use_ssl: bool,
    insecure: bool,
    verbose: bool,
    extra_verbose: bool,
):
    """
    Process batch requests against V2-compatible inference server.

    Currently, this is meant to be an entrypoint for the `mlserver infer ...` CLI.
    Note: this feature is currently experimental and API is subject to change.
    """
    start_time = timer()

    if transport == "grpc":
        raise click.BadParameter("The 'grpc' transport is not yet supported.")

    if extra_verbose:
        verbose = True
        logger.info("Running in extra verbose mode.")
    elif verbose:
        logger.info("Running in verbose mode.")

    headers = _preprocess_headers(request_headers)

    setup_logging(debug=verbose)
    logger.info(f"server url: {url}")
    logger.info(f"model name: {model_name}")
    logger.info(f"request headers: {headers}")
    logger.info(f"input file path: {input_data_path}")
    logger.info(f"output file path: {output_data_path}")
    logger.info(f"workers: {workers}")
    logger.info(f"retries: {retries}")
    logger.info(f"batch interval: {batch_interval}")
    logger.info(f"batch jitter: {batch_jitter}")
    logger.info(f"connection timeout: {timeout}")
    logger.info(f"micro-batch size: {batch_size}")

    if not _verify_write_access(output_data_path):
        raise click.BadParameter(
            f"Provided output file path '{output_data_path}' is not writable."
        )

    if insecure:
        ssl_context = False
    else:
        ssl_context = None

    triton_client = httpclient.InferenceServerClient(
        url=url,
        verbose=extra_verbose,
        conn_limit=workers,
        conn_timeout=timeout,
        ssl=use_ssl,
        ssl_context=ssl_context,
    )

    queue_in: asyncio.Queue[List[BatchInputItem]] = asyncio.Queue(2 * workers)
    queue_out: asyncio.Queue[List[BatchOutputItem]] = asyncio.Queue(2 * workers)

    consumers = []
    for worker_id in range(workers):
        consumer = asyncio.create_task(
            consume(
                model_name,
                worker_id,
                retries,
                batch_interval,
                batch_jitter,
                triton_client,
                headers,
                binary_data,
                extra_verbose,
                queue_in,
                queue_out,
            )
        )
        consumers.append(consumer)

    finalizer = asyncio.create_task(finalize(queue_out, output_data_path))

    await produce(queue_in, input_data_path, batch_size)
    await queue_in.join()
    await queue_out.join()

    for consumer in consumers:
        consumer.cancel()
    await asyncio.gather(*consumers, return_exceptions=True)

    finalizer.cancel()
    processed_instances = await finalizer
    logger.info(f"Total processed instances: {processed_instances}")

    await triton_client.close()

    logger.info(f"Time taken: {(timer()-start_time):.2f} seconds")
