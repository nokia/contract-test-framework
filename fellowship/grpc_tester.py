# Copyright 2021 Nokia
# Licensed under the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import os

from grpc_requests import Client
from grpc_requests import StubClient

from .endpoint_tester import EndpointTester
from .utilis import get_descriptor_name


class GrpcTester(EndpointTester):
    """Validates Rest endpoints based on contracts
    Attributes:
        contract_dir (str): Path to directory of contracts to validate
        contract_renderer (object): Contract render module used to fill the Jinja2
            template of the contracts.
    """
    _requests_arg_names = ['host', 'endpoint', 'port', 'function', 'package']

    def __init__(self, contract_dir: str):
        super().__init__(contract_dir)
        self.grpc_address = None

    def _make_request(self, contract_json):
        request_kwargs = self._construct_request_kwargs(contract_json)
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
        service_descriptor = get_descriptor_name(proto_path)
        grpc_endpoint = service_descriptor.services_by_name[
            request_kwargs["endpoint"]
        ]
        client = StubClient.get_by_endpoint(
            self.grpc_address,
            service_descriptors=[grpc_endpoint, ]
        )
        sub = client.service(service)
        grpc_function = getattr(sub, request_kwargs["function"])
        result = grpc_function(request_kwargs["request_data"])
        return result

    def _start_proto_path_from_contract(self, proto_path):
        return os.path.join(self.contract_dir, proto_path)
