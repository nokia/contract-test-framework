# Copyright 2021 Nokia
# Licensed under the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import os

from grpc_requests import Client
from grpc_requests import StubClient
from grpc_requests.client import get_by_endpoint, reset_cached_client

from .endpoint_tester import EndpointTester
from .utilis import get_grpc_service_descriptor


class GrpcTester(EndpointTester):
    """Validates gRPC endpoints based on contracts. Inherits EndpointTester

    Supports two different gRPC communication methods reflection and stub. In the stub
    method, the user must provide the corresponding proto so Fellowship can generate the
    stub for requests. If the gRPC server support reflection, you do not need the proto
    file, since Fellowship can directly request the endpoints returned by the reflection
    endpoint.

    Attributes:
        grpc_address (str): The address that the request targets. Format: ip:port
    """

    def __init__(self, contract_dir: str):
        super().__init__(contract_dir)
        self._grpc_address = None
        self._service = None

    def _make_request(self, contract_json):
        request_kwargs = contract_json["request"]
        self._construct_common_request_args(request_kwargs)
        self._check_if_service_in_cache()
        if contract_json['request']['method'] == "reflection":
            result = self._reflection_request(request_kwargs)
        else:
            result = self._stub_request(request_kwargs)
        return result

    def _construct_common_request_args(self, request_kwargs):
        self._grpc_address = request_kwargs['host'] + ":" + request_kwargs['port']
        self._service = request_kwargs["package"] + "." + request_kwargs["endpoint"]

    def _check_if_service_in_cache(self):
        client = get_by_endpoint(self._grpc_address)
        if self._service not in client.service_names:
            reset_cached_client()

    def _reflection_request(self, request_kwargs):
        client = Client.get_by_endpoint(self._grpc_address)
        service = request_kwargs["package"] + "." + request_kwargs["endpoint"]
        result = client.request(service,
                                request_kwargs["function"],
                                request_kwargs["data"])
        return result

    def _stub_request(self, request_kwargs):
        proto_path = self._start_proto_path_from_contract(request_kwargs["proto_file"])
        service_descriptor = get_grpc_service_descriptor(proto_path)
        grpc_endpoint = service_descriptor.DESCRIPTOR.services_by_name[
            request_kwargs["endpoint"]
        ]
        client = StubClient.get_by_endpoint(
            self._grpc_address,
            service_descriptors=[grpc_endpoint, ]
        )
        service_client = client.service(self._service)
        grpc_function = getattr(service_client, request_kwargs["function"])
        result = grpc_function(request_kwargs["data"])
        return result

    def _start_proto_path_from_contract(self, proto_path):
        return os.path.join(self.contract_dir, proto_path)
