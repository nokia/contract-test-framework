# Copyright 2021 Nokia
# Licensed under the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import os

from .contract_generator import ContractGenerator
from .utilis import get_grpc_service_descriptor


MOCK_FILL = {
    **{n: "Hello World!" for n in [9, 12, 14]},
    **{n: 123 for n in [3, 4, 5, 6, 7, 13, 15, 16, 17, 18]},
    **{n: 1.23 for n in [1, 2]},
    8: True
}


class GrpcGenerator:

    def __init__(self, proto_file: str) -> None:
        self.proto_file = proto_file
        self.proto = None
        self.descriptor = None
        self.message_dict = None

    def generate_grpc_contracts(self):
        self.descriptor = get_grpc_service_descriptor(self.proto_file)
        end_points = self._find_endpoints()
        self._create_contracts(end_points)

    def _find_endpoints(self):
        services_in_proto_file = dict(self.descriptor.DESCRIPTOR.services_by_name)
        self.message_dict = dict(self.descriptor.DESCRIPTOR.message_types_by_name)
        service_methods = self._get_service_methods(services_in_proto_file)
        output_messages = self._get_output_message_for_services(service_methods)
        json_message = self._get_messages_for_method(output_messages)
        return json_message

    @staticmethod
    def _get_service_methods(services_in_proto_file):
        service_methods = []
        for _, service_descriptor in services_in_proto_file.items():
            service_methods.append(dict(service_descriptor.methods_by_name))
        return service_methods

    @staticmethod
    def _get_output_message_for_services(service_list):
        method_dict = {}
        for service_method in service_list:
            for _, method_descriptor in service_method.items():
                method_dict[method_descriptor.full_name] = method_descriptor.output_type
        return method_dict

    def _get_messages_for_method(self, method_dict):
        json_messages = {}
        for message_name, message_descriptor in method_dict.items():
            json_messages[message_name] = self._message_to_dict(message_descriptor)
        return json_messages

    def _message_to_dict(self, message_descriptor):
        message_dict = {}
        for field in message_descriptor.fields:
            if field.message_type:
                message_dict[field.name] = self._message_to_dict(field.message_type)
            else:
                message_dict[field.name] = MOCK_FILL[field.cpp_type]
        return message_dict

    def _create_contracts(self, grpc_contract_dict):
        for request_string, request_response in grpc_contract_dict.items():
            request_dict = self._create_request_dict(request_string)
            contract_path = request_string.replace(".", "_") + ".json"
            generator = ContractGenerator(contract_path, "grpc")
            generator.generate_and_save_contract(request_dict, request_response)

    def _create_request_dict(self, request_string):
        request_dict = {}
        package, endpoint, function = request_string.split(".")
        request_dict["package"] = package
        request_dict["endpoint"] = endpoint
        request_dict["function"] = function
        request_dict["proto_file"] = os.path.join("protos", self.proto_file)
        request_dict["host"] = "{{ config.host }}"
        request_dict["port"] = "{{ config.port }}"
        request_dict["method"] = "{{ config.method }}"
        request_dict["data"] = "PLEASE FILL REQUEST AS A JSON HERE!"
        return request_dict
