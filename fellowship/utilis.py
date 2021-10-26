# Copyright 2021 Nokia
# Licensed under the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import os
import json
import sys
import yaml

from jsonschema import validate
from grpc import services


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def load_custom_schema(schema_file: str) -> dict:
    """Loads custom meta schema from the schemas directory

    Args:
        schema_file (str): Name of the schema file located in schemas directory

    Returns:
        dict: The loaded schema
    """
    schema_path = os.path.join(CURRENT_DIR, os.path.join("schemas", schema_file))
    with open(schema_path, encoding="UTF-8") as schema:
        return json.load(schema)


CUSTOM_REST_JSON_SCHEMA = load_custom_schema("rest_schema.json")
CUSTOM_GRPC_JSON_SCHEMA = load_custom_schema("grpc_schema.json")


def validate_contract(contract_dict: dict) -> None:
    """Validates contracts against custom meta json schema

    Meta scheme is based on the Draft7 from json schema with an extension for request
    dict. Which meta to use is based on contract_type field in schema that is being
    validated. If the field is missing defaults to REST.

    Args:
        contract_dict (dict):
    """
    contract_type = get_type_of_contract(contract_dict)
    if contract_type.lower() == "grpc":
        validate(contract_dict, CUSTOM_GRPC_JSON_SCHEMA)
    else:
        validate(contract_dict, CUSTOM_REST_JSON_SCHEMA)


def get_type_of_contract(contract_dict: dict) -> str:
    try:
        return contract_dict["contract_type"]
    except KeyError:
        return "rest"


def load_config():
    """Loads the configuration dictionary that is used to fill contracts

    Function loads the config yaml, given at the path of environment variable
    contract_test_config, if this variable is not present. It will load default config
    from configs/rest_config.yaml

    Returns:
        dict: configuration dict

    """
    try:
        config_path = os.environ['contract_test_config']
        return read_yaml(config_path)
    except KeyError:
        config_path = os.path.join(CURRENT_DIR, os.path.join("configs",
                                                             "rest_config.yaml"))
        return read_yaml(config_path)


def read_yaml(path: str) -> dict:
    """Loads yaml at given path

    Args:
        path (str): path to yaml file

    Returns:
        dict: dict loaded from yaml

    """
    with open(path, encoding="UTF-8") as yaml_file:
        return yaml.safe_load(yaml_file)


def get_grpc_service_descriptor(proto_file: str) -> object:
    """Compiles ard parses proto file to find service descriptor

    Function also need to add the directory of the proto file to sys path otherwise
    import of the compiled grpc module will fail.

    Args:
        proto_file (str): path to proto_file

    Returns:
        object: A grpc service descriptor
    """
    path_for_proto_import = os.path.dirname(os.path.abspath(proto_file))
    sys.path.append(path_for_proto_import)
    grpc_services = services("test.proto")
    descriptor_name = get_descriptor_name(proto_file)
    return getattr(grpc_services, descriptor_name)


def get_descriptor_name(proto_file: str) -> str:
    """Returns the name of the grpc descriptor based on protocol buffer file

    Args:
        proto_file (str): path to proto_file

    Returns:
        str: Name of the descriptor service
    """
    descriptor_name = os.path.basename(proto_file).split(".")[0]
    descriptor_name += "__pb2"
    return descriptor_name
