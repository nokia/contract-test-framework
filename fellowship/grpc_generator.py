# Copyright 2021 Nokia
# Licensed under the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import os

from .contract_generator import ContractGenerator
from .utilis import get_grpc_service_descriptor


# CPP_TYPE_MAP is a dictionary that maps cpp_types to placeholder values for JSON_SCHEMA
# generation. Reference for cpp_types:
# https://developers.google.com/protocol-buffers/docs/reference/cpp/google.protobuf.descriptor#FieldDescriptor.Type.details
CPP_TYPE_MAP = {
    **{n: "" for n in [9, 12, 14]},
    **{n: 1 for n in [3, 4, 5, 6, 7, 13, 15, 16, 17, 18]},
    **{n: 1.0 for n in [1, 2]},
    8: True
}


class GrpcGenerator:
    """Generates a skeleton for the gRPC, as a base for generation it uses the proto file

    Goes through a proto file, finding all endpoints and their responses, generates a
    contract per endpoint. Supports also nested message objects. The generation is done
    by complying the proto file and parsing the corresponding descriptor objects. After
    the expected response is obtained it calls ContractGenerator

    Attributes:
        proto_file (str): The proto file that generation will be based on.
        output_dir (str): Directory to output the contracts to. Default value is current
            directory.
    """
    _config_values = ["host", "port", "method"]

    def __init__(self, proto_file: str, output_dir: str = "") -> None:
        self.proto_file = proto_file
        self.output_dir = output_dir
        self._descriptor = None

    def generate_grpc_contracts(self):
        """ Function that generates a new contracts and saves it to output_dir

        Makes a contract for each end point available in the proto file and saves it to
        the output dir. The name convention is package_endpoint_function.json
        """
        self._descriptor = get_grpc_service_descriptor(self.proto_file)
        end_points = self._find_endpoints()
        self._create_contracts(end_points)

    def _find_endpoints(self):
        services_in_proto_file = dict(self._descriptor.DESCRIPTOR.services_by_name)
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
                message_dict[field.name] = self._check_if_list(
                    field.label,
                    self._message_to_dict(field.message_type)
                )
            else:
                message_dict[field.name] = self._check_if_list(
                    field.label,
                    CPP_TYPE_MAP[field.cpp_type]
                )
        return message_dict

    @staticmethod
    def _check_if_list(label, value):
        if label == 3:
            return [value]
        return value

    def _create_contracts(self, grpc_contract_dict):
        for request_string, request_response in grpc_contract_dict.items():
            request_dict = self._create_request_dict(request_string)
            contract_file = request_string.replace(".", "_") + ".json"
            contract_path = os.path.join(self.output_dir, contract_file)
            generator = ContractGenerator(contract_path, "grpc")
            generator.generate_and_save_contract(request_dict, request_response)

    def _create_request_dict(self, request_string):
        request_dict = {}
        package, endpoint, function = request_string.split(".")
        request_dict["package"] = package
        request_dict["endpoint"] = endpoint
        request_dict["function"] = function
        request_dict["proto_file"] = os.path.join("protos",
                                                  os.path.basename(self.proto_file))
        self._add_config_to_requests_dict(request_dict)
        request_dict["data"] = "PLEASE FILL REQUEST AS A JSON HERE!"
        return request_dict

    def _add_config_to_requests_dict(self, request_dict):
        for config_value in self._config_values:
            request_dict[config_value] = f"{{{{ config.{config_value} }}}}"
