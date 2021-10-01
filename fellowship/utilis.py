# Copyright 2021 Nokia
# Licensed under the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import os
import json
import yaml

from jsonschema import validate


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
SCHEMA_PATH = os.path.join(CURRENT_DIR, os.path.join("schemas", "rest_schema.json"))
with open(SCHEMA_PATH, encoding="UTF-8") as schema:
    CUSTOM_JSON_SCHEMA = json.load(schema)


def validate_contract(contract_dict: dict) -> None:
    """Validates contracts against custom meta json schema

    Meta scheme is based on the Draft7 from json schema with an extension for request
    dict.

    Args:
        contract_dict (dict):
    """
    validate(contract_dict, CUSTOM_JSON_SCHEMA)


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


def read_yaml(path):
    """Loads yaml at given path

    Args:
        path (str): path to yaml file

    Returns:
        dict: dict loaded from yaml

    """
    with open(path, encoding="UTF-8") as yaml_file:
        return yaml.safe_load(yaml_file)
