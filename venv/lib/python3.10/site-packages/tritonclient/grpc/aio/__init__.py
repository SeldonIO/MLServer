# Copyright 2022, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#  * Neither the name of NVIDIA CORPORATION nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from tritonclient.grpc import *
from tritonclient.grpc import _get_inference_request, _grpc_compression_type

# In case user try to import dependency from here
from tritonclient.grpc import InferInput, InferRequestedOutput


class InferenceServerClient():
    """This feature is currently in beta and may be subject to change.
    
    An analogy of the tritonclient.grpc.InferenceServerClient to enable 
    calling via asyncio syntax. The object is intended to be used by a single 
    thread and simultaneously calling methods with different threads is not 
    supported and can cause undefined behavior.

    """

    def __init__(self,
                 url,
                 verbose=False,
                 ssl=False,
                 root_certificates=None,
                 private_key=None,
                 certificate_chain=None,
                 creds=None,
                 keepalive_options=None,
                 channel_args=None):

        # Explicitly check "is not None" here to support passing an empty
        # list to specify setting no channel arguments.
        if channel_args is not None:
            channel_opt = channel_args
        else:
            # Use GRPC KeepAlive client defaults if unspecified
            if not keepalive_options:
                keepalive_options = KeepAliveOptions()

            # To specify custom channel_opt, see the channel_args parameter.
            channel_opt = [
                ('grpc.max_send_message_length', MAX_GRPC_MESSAGE_SIZE),
                ('grpc.max_receive_message_length', MAX_GRPC_MESSAGE_SIZE),
                ('grpc.keepalive_time_ms', keepalive_options.keepalive_time_ms),
                ('grpc.keepalive_timeout_ms',
                 keepalive_options.keepalive_timeout_ms),
                ('grpc.keepalive_permit_without_calls',
                 keepalive_options.keepalive_permit_without_calls),
                ('grpc.http2.max_pings_without_data',
                 keepalive_options.http2_max_pings_without_data),
            ]

        if creds:
            self._channel = grpc.aio.secure_channel(url,
                                                    creds,
                                                    options=channel_opt)
        elif ssl:
            rc_bytes = pk_bytes = cc_bytes = None
            if root_certificates is not None:
                with open(root_certificates, 'rb') as rc_fs:
                    rc_bytes = rc_fs.read()
            if private_key is not None:
                with open(private_key, 'rb') as pk_fs:
                    pk_bytes = pk_fs.read()
            if certificate_chain is not None:
                with open(certificate_chain, 'rb') as cc_fs:
                    cc_bytes = cc_fs.read()
            creds = grpc.ssl_channel_credentials(root_certificates=rc_bytes,
                                                 private_key=pk_bytes,
                                                 certificate_chain=cc_bytes)
            self._channel = grpc.aio.secure_channel(url,
                                                    creds,
                                                    options=channel_opt)
        else:
            self._channel = grpc.aio.insecure_channel(url, options=channel_opt)
        self._client_stub = service_pb2_grpc.GRPCInferenceServiceStub(
            self._channel)
        self._verbose = verbose

    async def __aenter__(self):
        return self

    async def __aexit__(self, type, value, traceback):
        await self.close()

    async def close(self):
        """Close the client. Any future calls to server
        will result in an Error.

        """
        await self._channel.close()

    async def is_server_live(self, headers=None):
        """Refer to tritonclient.grpc.InferenceServerClient

        """
        if headers is not None:
            metadata = headers.items()
        else:
            metadata = ()
        try:
            request = service_pb2.ServerLiveRequest()
            if self._verbose:
                print("is_server_live, metadata {}\n{}".format(
                    metadata, request))
            response = await self._client_stub.ServerLive(request=request,
                                                          metadata=metadata)
            if self._verbose:
                print(response)
            return response.live
        except grpc.RpcError as rpc_error:
            raise_error_grpc(rpc_error)

    async def is_server_ready(self, headers=None):
        """Refer to tritonclient.grpc.InferenceServerClient

        """
        if headers is not None:
            metadata = headers.items()
        else:
            metadata = ()
        try:
            request = service_pb2.ServerReadyRequest()
            if self._verbose:
                print("is_server_ready, metadata {}\n{}".format(
                    metadata, request))
            response = await self._client_stub.ServerReady(request=request,
                                                           metadata=metadata)
            if self._verbose:
                print(response)
            return response.ready
        except grpc.RpcError as rpc_error:
            raise_error_grpc(rpc_error)

    async def is_model_ready(self, model_name, model_version="", headers=None):
        """Refer to tritonclient.grpc.InferenceServerClient

        """
        if headers is not None:
            metadata = headers.items()
        else:
            metadata = ()
        try:
            if type(model_version) != str:
                raise_error("model version must be a string")
            request = service_pb2.ModelReadyRequest(name=model_name,
                                                    version=model_version)
            if self._verbose:
                print("is_model_ready, metadata {}\n{}".format(
                    metadata, request))
            response = await self._client_stub.ModelReady(request=request,
                                                          metadata=metadata)
            if self._verbose:
                print(response)
            return response.ready
        except grpc.RpcError as rpc_error:
            raise_error_grpc(rpc_error)

    async def get_server_metadata(self, headers=None, as_json=False):
        """Refer to tritonclient.grpc.InferenceServerClient

        """
        if headers is not None:
            metadata = headers.items()
        else:
            metadata = ()
        try:
            request = service_pb2.ServerMetadataRequest()
            if self._verbose:
                print("get_server_metadata, metadata {}\n{}".format(
                    metadata, request))
            response = await self._client_stub.ServerMetadata(request=request,
                                                              metadata=metadata)
            if self._verbose:
                print(response)
            if as_json:
                return json.loads(
                    MessageToJson(response, preserving_proto_field_name=True))
            else:
                return response
        except grpc.RpcError as rpc_error:
            raise_error_grpc(rpc_error)

    async def get_model_metadata(self,
                                 model_name,
                                 model_version="",
                                 headers=None,
                                 as_json=False):
        """Refer to tritonclient.grpc.InferenceServerClient

        """
        if headers is not None:
            metadata = headers.items()
        else:
            metadata = ()
        try:
            if type(model_version) != str:
                raise_error("model version must be a string")
            request = service_pb2.ModelMetadataRequest(name=model_name,
                                                       version=model_version)
            if self._verbose:
                print("get_model_metadata, metadata {}\n{}".format(
                    metadata, request))
            response = await self._client_stub.ModelMetadata(request=request,
                                                             metadata=metadata)
            if self._verbose:
                print(response)
            if as_json:
                return json.loads(
                    MessageToJson(response, preserving_proto_field_name=True))
            else:
                return response
        except grpc.RpcError as rpc_error:
            raise_error_grpc(rpc_error)

    async def get_model_config(self,
                               model_name,
                               model_version="",
                               headers=None,
                               as_json=False):
        """Refer to tritonclient.grpc.InferenceServerClient

        """
        if headers is not None:
            metadata = headers.items()
        else:
            metadata = ()
        try:
            if type(model_version) != str:
                raise_error("model version must be a string")
            request = service_pb2.ModelConfigRequest(name=model_name,
                                                     version=model_version)
            if self._verbose:
                print("get_model_config, metadata {}\n{}".format(
                    metadata, request))
            response = await self._client_stub.ModelConfig(request=request,
                                                           metadata=metadata)
            if self._verbose:
                print(response)
            if as_json:
                return json.loads(
                    MessageToJson(response, preserving_proto_field_name=True))
            else:
                return response
        except grpc.RpcError as rpc_error:
            raise_error_grpc(rpc_error)

    async def get_model_repository_index(self, headers=None, as_json=False):
        """Refer to tritonclient.grpc.InferenceServerClient

        """
        if headers is not None:
            metadata = headers.items()
        else:
            metadata = ()
        try:
            request = service_pb2.RepositoryIndexRequest()
            if self._verbose:
                print("get_model_repository_index, metadata {}\n{}".format(
                    metadata, request))
            response = await self._client_stub.RepositoryIndex(
                request=request, metadata=metadata)
            if self._verbose:
                print(response)
            if as_json:
                return json.loads(
                    MessageToJson(response, preserving_proto_field_name=True))
            else:
                return response
        except grpc.RpcError as rpc_error:
            raise_error_grpc(rpc_error)

    async def load_model(self,
                         model_name,
                         headers=None,
                         config=None,
                         files=None):
        """Refer to tritonclient.grpc.InferenceServerClient

        """
        if headers is not None:
            metadata = headers.items()
        else:
            metadata = ()
        try:
            request = service_pb2.RepositoryModelLoadRequest(
                model_name=model_name)
            if config is not None:
                request.parameters["config"].string_param = config
            if self._verbose:
                # Don't print file content which can be large
                print("load_model, metadata {}\noverride files omitted:\n{}".
                      format(metadata, request))
            if files is not None:
                for path, content in files.items():
                    request.parameters[path].bytes_param = content
            await self._client_stub.RepositoryModelLoad(request=request,
                                                        metadata=metadata)
            if self._verbose:
                print("Loaded model '{}'".format(model_name))
        except grpc.RpcError as rpc_error:
            raise_error_grpc(rpc_error)

    async def unload_model(self,
                           model_name,
                           headers=None,
                           unload_dependents=False):
        """Refer to tritonclient.grpc.InferenceServerClient

        """
        if headers is not None:
            metadata = headers.items()
        else:
            metadata = ()
        try:
            request = service_pb2.RepositoryModelUnloadRequest(
                model_name=model_name)
            request.parameters[
                'unload_dependents'].bool_param = unload_dependents
            if self._verbose:
                print("unload_model, metadata {}\n{}".format(metadata, request))
            await self._client_stub.RepositoryModelUnload(request=request,
                                                          metadata=metadata)
            if self._verbose:
                print("Unloaded model '{}'".format(model_name))
        except grpc.RpcError as rpc_error:
            raise_error_grpc(rpc_error)

    async def get_inference_statistics(self,
                                       model_name="",
                                       model_version="",
                                       headers=None,
                                       as_json=False):
        """Refer to tritonclient.grpc.InferenceServerClient

        """
        if headers is not None:
            metadata = headers.items()
        else:
            metadata = ()
        try:
            if type(model_version) != str:
                raise_error("model version must be a string")
            request = service_pb2.ModelStatisticsRequest(name=model_name,
                                                         version=model_version)
            if self._verbose:
                print("get_inference_statistics, metadata {}\n{}".format(
                    metadata, request))
            response = await self._client_stub.ModelStatistics(
                request=request, metadata=metadata)
            if self._verbose:
                print(response)
            if as_json:
                return json.loads(
                    MessageToJson(response, preserving_proto_field_name=True))
            else:
                return response
        except grpc.RpcError as rpc_error:
            raise_error_grpc(rpc_error)

    async def update_trace_settings(self,
                                    model_name=None,
                                    settings={},
                                    headers=None,
                                    as_json=False):
        """Refer to tritonclient.grpc.InferenceServerClient

        """
        if headers is not None:
            metadata = headers.items()
        else:
            metadata = ()
        try:
            request = service_pb2.TraceSettingRequest()
            if (model_name is not None) and (model_name != ""):
                request.model_name = model_name
            for key, value in settings.items():
                if value is None:
                    request.settings[key]
                else:
                    request.settings[key].value.extend(
                        value if isinstance(value, list) else [value])

            if self._verbose:
                print("update_trace_settings, metadata {}\n{}".format(
                    metadata, request))
            response = await self._client_stub.TraceSetting(request=request,
                                                            metadata=metadata)
            if self._verbose:
                print(response)
            if as_json:
                return json.loads(
                    MessageToJson(response, preserving_proto_field_name=True))
            else:
                return response
        except grpc.RpcError as rpc_error:
            raise_error_grpc(rpc_error)

    async def get_trace_settings(self,
                                 model_name=None,
                                 headers=None,
                                 as_json=False):
        """Refer to tritonclient.grpc.InferenceServerClient

        """
        if headers is not None:
            metadata = headers.items()
        else:
            metadata = ()
        try:
            request = service_pb2.TraceSettingRequest()
            if (model_name is not None) and (model_name != ""):
                request.model_name = model_name
            if self._verbose:
                print("get_trace_settings, metadata {}\n{}".format(
                    metadata, request))
            response = await self._client_stub.TraceSetting(request=request,
                                                            metadata=metadata)
            if self._verbose:
                print(response)
            if as_json:
                return json.loads(
                    MessageToJson(response, preserving_proto_field_name=True))
            else:
                return response
        except grpc.RpcError as rpc_error:
            raise_error_grpc(rpc_error)

    async def update_log_settings(self, settings, headers=None, as_json=False):
        """Refer to tritonclient.grpc.InferenceServerClient
        """
        if headers is not None:
            metadata = headers.items()
        else:
            metadata = ()
        try:
            request = service_pb2.LogSettingsRequest()
            for key, value in settings.items():
                if value is None:
                    request.settings[key]
                else:
                    if key == "log_file" or key == "log_format":
                        request.settings[key].string_param = value
                    elif key == "log_verbose_level":
                        request.settings[key].uint32_param = value
                    else:
                        request.settings[key].bool_param = value

            if self._verbose:
                print("update_log_settings, metadata {}\n{}".format(
                    metadata, request))
            response = await self._client_stub.LogSettings(request=request,
                                                           metadata=metadata)
            if self._verbose:
                print(response)
            if as_json:
                return json.loads(
                    MessageToJson(response, preserving_proto_field_name=True))
            else:
                return response
        except grpc.RpcError as rpc_error:
            raise_error_grpc(rpc_error)

    async def get_log_settings(self, headers=None, as_json=False):
        """Refer to tritonclient.grpc.InferenceServerClient
        """
        if headers is not None:
            metadata = headers.items()
        else:
            metadata = ()
        try:
            request = service_pb2.LogSettingsRequest()
            if self._verbose:
                print("get_log_settings, metadata {}\n{}".format(
                    metadata, request))
            response = await self._client_stub.LogSettings(request=request,
                                                           metadata=metadata)
            if self._verbose:
                print(response)
            if as_json:
                return json.loads(
                    MessageToJson(response, preserving_proto_field_name=True))
            else:
                return response
        except grpc.RpcError as rpc_error:
            raise_error_grpc(rpc_error)

    async def get_system_shared_memory_status(self,
                                              region_name="",
                                              headers=None,
                                              as_json=False):
        """Refer to tritonclient.grpc.InferenceServerClient

        """
        if headers is not None:
            metadata = headers.items()
        else:
            metadata = ()
        try:
            request = service_pb2.SystemSharedMemoryStatusRequest(
                name=region_name)
            if self._verbose:
                print("get_system_shared_memory_status, metadata {}\n{}".format(
                    metadata, request))
            response = await self._client_stub.SystemSharedMemoryStatus(
                request=request, metadata=metadata)
            if self._verbose:
                print(response)
            if as_json:
                return json.loads(
                    MessageToJson(response, preserving_proto_field_name=True))
            else:
                return response
        except grpc.RpcError as rpc_error:
            raise_error_grpc(rpc_error)

    async def register_system_shared_memory(self,
                                            name,
                                            key,
                                            byte_size,
                                            offset=0,
                                            headers=None):
        """Refer to tritonclient.grpc.InferenceServerClient

        """
        if headers is not None:
            metadata = headers.items()
        else:
            metadata = ()
        try:
            request = service_pb2.SystemSharedMemoryRegisterRequest(
                name=name, key=key, offset=offset, byte_size=byte_size)
            if self._verbose:
                print("register_system_shared_memory, metadata {}\n{}".format(
                    metadata, request))
            await self._client_stub.SystemSharedMemoryRegister(
                request=request, metadata=metadata)
            if self._verbose:
                print("Registered system shared memory with name '{}'".format(
                    name))
        except grpc.RpcError as rpc_error:
            raise_error_grpc(rpc_error)

    async def unregister_system_shared_memory(self, name="", headers=None):
        """Refer to tritonclient.grpc.InferenceServerClient

        """
        if headers is not None:
            metadata = headers.items()
        else:
            metadata = ()
        try:
            request = service_pb2.SystemSharedMemoryUnregisterRequest(name=name)
            if self._verbose:
                print("unregister_system_shared_memory, metadata {}\n{}".format(
                    metadata, request))
            await self._client_stub.SystemSharedMemoryUnregister(
                request=request, metadata=metadata)
            if self._verbose:
                if name != "":
                    print("Unregistered system shared memory with name '{}'".
                          format(name))
                else:
                    print("Unregistered all system shared memory regions")
        except grpc.RpcError as rpc_error:
            raise_error_grpc(rpc_error)

    async def get_cuda_shared_memory_status(self,
                                            region_name="",
                                            headers=None,
                                            as_json=False):
        """Refer to tritonclient.grpc.InferenceServerClient

        """

        if headers is not None:
            metadata = headers.items()
        else:
            metadata = ()
        try:
            request = service_pb2.CudaSharedMemoryStatusRequest(
                name=region_name)
            if self._verbose:
                print("get_cuda_shared_memory_status, metadata {}\n{}".format(
                    metadata, request))
            response = await self._client_stub.CudaSharedMemoryStatus(
                request=request, metadata=metadata)
            if self._verbose:
                print(response)
            if as_json:
                return json.loads(
                    MessageToJson(response, preserving_proto_field_name=True))
            else:
                return response
        except grpc.RpcError as rpc_error:
            raise_error_grpc(rpc_error)

    async def register_cuda_shared_memory(self,
                                          name,
                                          raw_handle,
                                          device_id,
                                          byte_size,
                                          headers=None):
        """Refer to tritonclient.grpc.InferenceServerClient

        """
        if headers is not None:
            metadata = headers.items()
        else:
            metadata = ()
        try:
            request = service_pb2.CudaSharedMemoryRegisterRequest(
                name=name,
                raw_handle=base64.b64decode(raw_handle),
                device_id=device_id,
                byte_size=byte_size)
            if self._verbose:
                print("register_cuda_shared_memory, metadata {}\n{}".format(
                    metadata, request))
            await self._client_stub.CudaSharedMemoryRegister(request=request,
                                                             metadata=metadata)
            if self._verbose:
                print(
                    "Registered cuda shared memory with name '{}'".format(name))
        except grpc.RpcError as rpc_error:
            raise_error_grpc(rpc_error)

    async def unregister_cuda_shared_memory(self, name="", headers=None):
        """Refer to tritonclient.grpc.InferenceServerClient

        """
        if headers is not None:
            metadata = headers.items()
        else:
            metadata = ()
        try:
            request = service_pb2.CudaSharedMemoryUnregisterRequest(name=name)
            if self._verbose:
                print("unregister_cuda_shared_memory, metadata {}\n{}".format(
                    metadata, request))
            await self._client_stub.CudaSharedMemoryUnregister(
                request=request, metadata=metadata)
            if self._verbose:
                if name != "":
                    print(
                        "Unregistered cuda shared memory with name '{}'".format(
                            name))
                else:
                    print("Unregistered all cuda shared memory regions")
        except grpc.RpcError as rpc_error:
            raise_error_grpc(rpc_error)

    async def infer(self,
                    model_name,
                    inputs,
                    model_version="",
                    outputs=None,
                    request_id="",
                    sequence_id=0,
                    sequence_start=False,
                    sequence_end=False,
                    priority=0,
                    timeout=None,
                    client_timeout=None,
                    headers=None,
                    compression_algorithm=None):
        """Refer to tritonclient.grpc.InferenceServerClient

        """

        if headers is not None:
            metadata = headers.items()
        else:
            metadata = ()

        if type(model_version) != str:
            raise_error("model version must be a string")

        request = _get_inference_request(model_name=model_name,
                                         inputs=inputs,
                                         model_version=model_version,
                                         request_id=request_id,
                                         outputs=outputs,
                                         sequence_id=sequence_id,
                                         sequence_start=sequence_start,
                                         sequence_end=sequence_end,
                                         priority=priority,
                                         timeout=timeout)
        if self._verbose:
            print("infer, metadata {}\n{}".format(metadata, request))

        try:
            response = await self._client_stub.ModelInfer(
                request=request,
                metadata=metadata,
                timeout=client_timeout,
                compression=_grpc_compression_type(compression_algorithm))
            if self._verbose:
                print(response)
            result = InferResult(response)
            return result
        except grpc.RpcError as rpc_error:
            raise_error_grpc(rpc_error)

    async def stream_infer(self,
                           inputs_iterator,
                           stream_timeout=None,
                           headers=None,
                           compression_algorithm=None):
        """Runs an asynchronous inference over gRPC bi-directional streaming
        API.

        Parameters
        ----------
        inputs_iterator : async_generator
            Async iterator that yields a dict(s) consists of the input 
            parameters to the async_stream_infer function defined in 
            tritonclient.grpc.InferenceServerClient.
        stream_timeout : float
            Optional stream timeout. The stream will be closed once the
            specified timeout expires.
        headers: dict
            Optional dictionary specifying additional HTTP headers to include 
            in the request.
        compression_algorithm : str
            Optional grpc compression algorithm to be used on client side.
            Currently supports "deflate", "gzip" and None. By default, no
            compression is used.

        Returns
        -------
        async_generator
            Yield tuple holding (InferResult, InferenceServerException) objects.

        Raises
        ------
        InferenceServerException
            If inputs_iterator does not yield the correct input.

        """
        if headers is not None:
            metadata = headers.items()
        else:
            metadata = ()

        async def _request_iterator(inputs_iterator):
            # Internal iterator for converting into grpc request
            async for inputs in inputs_iterator:
                if type(inputs) != dict:
                    raise_error("inputs_iterator is not yielding a dict")
                if "model_name" not in inputs or "inputs" not in inputs:
                    raise_error(
                        "model_name and/or inputs is missing from inputs_iterator's yielded dict"
                    )
                if "model_version" not in inputs:
                    inputs["model_version"] = ""
                if type(inputs["model_version"]) != str:
                    raise_error("model_version must be a string")
                if "outputs" not in inputs:
                    inputs["outputs"] = None
                if "request_id" not in inputs:
                    inputs["request_id"] = ""
                if "sequence_id" not in inputs:
                    inputs["sequence_id"] = 0
                if "sequence_start" not in inputs:
                    inputs["sequence_start"] = False
                if "sequence_end" not in inputs:
                    inputs["sequence_end"] = False
                if "priority" not in inputs:
                    inputs["priority"] = 0
                if "timeout" not in inputs:
                    inputs["timeout"] = None
                yield _get_inference_request(
                    model_name=inputs["model_name"],
                    inputs=inputs["inputs"],
                    model_version=inputs["model_version"],
                    request_id=inputs["request_id"],
                    outputs=inputs["outputs"],
                    sequence_id=inputs["sequence_id"],
                    sequence_start=inputs["sequence_start"],
                    sequence_end=inputs["sequence_end"],
                    priority=inputs["priority"],
                    timeout=inputs["timeout"])

        try:
            response_iterator = self._client_stub.ModelStreamInfer(
                _request_iterator(inputs_iterator),
                metadata=metadata,
                timeout=stream_timeout,
                compression=_grpc_compression_type(compression_algorithm))
            async for response in response_iterator:
                if self._verbose:
                    print(response)
                result = error = None
                if response.error_message != "":
                    error = InferenceServerException(msg=response.error_message)
                else:
                    result = InferResult(response.infer_response)
                yield (result, error)
        except grpc.RpcError as rpc_error:
            raise_error_grpc(rpc_error)
