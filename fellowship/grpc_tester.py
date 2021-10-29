# Copyright 2021 Nokia
# Licensed under the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import os

from grpc_requests import Client
from grpc_requests import StubClient

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
        self.grpc_address = None

    def _make_request(self, contract_json):
        request_kwargs = contract_json["request"]
        self.grpc_address = request_kwargs['host'] + ":" + request_kwargs['port']
        if contract_json['request']['method'] == "reflection":
            result = self._reflection_request(request_kwargs)
        else:
            result = self._stub_request(request_kwargs)
        return result

    def _reflection_request(self, request_kwargs):
        client = Client.get_by_endpoint(self.grpc_address)
        service = request_kwargs["package"] + "." + request_kwargs["endpoint"]
        result = client.request(service,
                                request_kwargs["function"],
                                request_kwargs["data"])
        return result

    def _stub_request(self, request_kwargs):
        package = request_kwargs["package"]
        service = package + "." + request_kwargs["endpoint"]
        proto_path = self._start_proto_path_from_contract(request_kwargs["proto_file"])
        service_descriptor = get_grpc_service_descriptor(proto_path)
        grpc_endpoint = service_descriptor.DESCRIPTOR.services_by_name[
            request_kwargs["endpoint"]
        ]
        client = StubClient.get_by_endpoint(
            self.grpc_address,
            service_descriptors=[grpc_endpoint, ]
        )
        service_client = client.service(service)
        grpc_function = getattr(service_client, request_kwargs["function"])
        result = grpc_function(request_kwargs["data"])
        return result

    def _start_proto_path_from_contract(self, proto_path):
        return os.path.join(self.contract_dir, proto_path)
