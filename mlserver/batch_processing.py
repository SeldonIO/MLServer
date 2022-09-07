from functools import wraps
import tritonclient.http.aio as httpclient

import asyncio
import aiofiles
import logging
import click
import json
import orjson

import numpy as np

from mlserver.types import InferenceRequest
from mlserver.codecs import NumpyCodec

from time import perf_counter as timer


INFER_LOG_LEVEL = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
}

logger = logging.getLogger(__name__)


# Monkey patching is required for error responses coming from MLServer.
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
            return httpclient.InferenceServerException(msg=json.dumps(error_response["detail"]))
    else:
        return None


httpclient._get_error = _get_error
del _get_error


def click_async(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


def setup_logging(log_level: str):
    LOG_FORMAT = (
        "%(asctime)s - batch_processor.py:%(lineno)s - %(levelname)s:  %(message)s"
    )
    logging.basicConfig(level=INFER_LOG_LEVEL[log_level], format=LOG_FORMAT)


def inference_request_to_triton(inference_request: InferenceRequest, binary_data: bool):
    inputs = []
    for request_input in inference_request.inputs or []:
        new_input = httpclient.InferInput(
            request_input.name, request_input.shape, request_input.datatype
        )
        new_input.set_data_from_numpy(
            NumpyCodec.decode_input(request_input),
            binary_data=binary_data,
        )
        inputs.append(new_input)

    outputs = []
    for request_output in inference_request.outputs or []:
        new_output = httpclient.InferRequestedOutput(
            request_output.name, binary_data=binary_data
        )
        outputs.append(new_output)

    return inputs, outputs


def serialize_triton_infer_result(triton_output: httpclient.InferResult):
    response = triton_output.get_response()
    for (n, output) in enumerate(response["outputs"]):
        data = triton_output.as_numpy(output["name"])
        response["outputs"][n]["data"] = data.flatten().tolist()

        # Removing "binary_data_size" parameters as now this is 1-D list
        if output["parameters"] is not None and "binary_data_size" in output["parameters"]:
            del response["outputs"][n]["parameters"]["binary_data_size"]

    return orjson.dumps(response)


async def produce(queue: asyncio.Queue, fname: str):
    async with aiofiles.open(fname) as f:
        async for line in f:
            await queue.put(line)


async def finalize(queue: asyncio.Queue, fname: str):
    # TODO: Test if output directory is writtable, sysexit otherwise.
    async with aiofiles.open(fname, "wb") as f:
        while True:
            item = await queue.get()
            try:
                output = serialize_triton_infer_result(item)
                await f.write(output)
                await f.write(b"\n")
            except Exception as e:
                logger.error(f"Failed to finalize task: {e}")
            queue.task_done()


async def consume(
    model_name: str,
    worker_id: int,
    triton_client: httpclient.InferenceServerClient,
    queue_in: asyncio.Queue,
    queue_out: asyncio.Queue,
    binary_payloads: bool,
):
    while True:
        item = await queue_in.get()
        inference_request = InferenceRequest.parse_obj(orjson.loads(item))
        print(f"consumer {worker_id}: request:", inference_request.inputs[0].shape)
        inputs, outputs = inference_request_to_triton(
            inference_request, binary_payloads
        )

        headers = {"content-type": "application/json"}
        try:
            data = await triton_client.infer(model_name, inputs, outputs=outputs, headers=headers)
            print(f"consumer {worker_id}: received response")
            await queue_out.put(data)
        except Exception as e:
            logger.error(f"Failed to process task: {e}")
        queue_in.task_done()


async def process_batch(
    model_name, url, workers, verbose, input_file_path, output_file_path, log_level, binary_payloads
):
    start_time = timer()
    setup_logging(log_level)
    logger.info(f"Server url: {url}")
    logger.info(f"input file path: {input_file_path}")
    logger.info(f"output file path: {output_file_path}")
    if verbose:
        logger.info("Running in verbose mode.")

    triton_client = httpclient.InferenceServerClient(
        url=url,
        verbose=verbose,
        conn_limit=workers,
    )

    queue_in = asyncio.Queue(2 * workers)
    queue_out = asyncio.Queue(2 * workers)

    consumers = []
    for worker_id in range(workers):
        consumer = asyncio.create_task(
            consume(model_name, worker_id, triton_client, queue_in, queue_out, binary_payloads)
        )
        consumers.append(consumer)

    finalizer = asyncio.create_task(finalize(queue_out, output_file_path))

    await produce(queue_in, input_file_path)
    await queue_in.join()
    await queue_out.join()

    for consumer in consumers:
        consumer.cancel()

    finalizer.cancel()

    await asyncio.gather(*consumers, finalizer, return_exceptions=True)

    await triton_client.close()

    logger.info(f"Time taken: {(timer()-start_time):.2f} seconds")
