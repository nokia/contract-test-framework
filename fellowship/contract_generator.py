# Copyright 2021 Nokia
# Licensed under the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import json
import logging
import os
from urllib.parse import urlparse

from genson import SchemaBuilder

from .contract_renderer import ContractRenderer
from .strict_schema_builder import StrictSchemaBuilder


LOGGER = logging.getLogger(__name__)


class ContractGenerator:
    """Generates a json contract based on a request and its expected output.

    Attributes:
        contract_path (str): The path of file that will be generated
        type_of_contract (str): The type to write to contract in field contract_type
            can be either rest or grpc. Default value: rest
    """

    def __init__(self, output_path: str, type_of_contract: str = "rest") -> None:
        self.contract_path = output_path
        self.type_of_contract = type_of_contract
        self.contract_renderer = ContractRenderer(os.path.dirname(output_path))
        self.schema_builder = SchemaBuilder()

    def set_type_of_schema_builder(self, type_of_schema_builder: str = "type") -> None:
        """Sets the type of schema builder can be either type or strict

        Type builder is the default and generates the contract with type validation. The
        Other type of builder supported is strict which will generate contract with
        expected value for each field.

        Args:
            type_of_schema_builder (str): The type of builder to use when generating
                schema can be either type or strict. Default value: type
        """
        if type_of_schema_builder == "strict":
            self.schema_builder = StrictSchemaBuilder()
        else:
            self.schema_builder = SchemaBuilder()

    def generate_and_save_contract(self, request_kwargs: dict, expected_json: dict) \
            -> None:
        """ Function that generates a new contract and saves it to specified location

        Args:
            request_kwargs (dict): A dictionary that describes the request that should
                return the expected_json. The dictionary needs to contain url (at least
                endpoint) and method. Optional parameters include headers and data
            expected_json (dict): Is the Json response that is expected when the request
                from the request_kwargs dictionary is sent.
        """
        contract_json = self._generate_contract(request_kwargs, expected_json)
        self._save_contract(contract_json)

    def _generate_contract(self, request_kwargs, expected_json):
        if self.type_of_contract.lower() == "rest":
            self._check_request_kwargs(request_kwargs)
        self.schema_builder.add_schema({'contract_type': self.type_of_contract,
                                        'request': {**request_kwargs}})
        self.schema_builder.add_object(expected_json)
        LOGGER.info("The generated schema: %s \nSaved to file: %s",
                    self.schema_builder.to_json(indent=4), self.contract_path)
        return self.schema_builder.to_schema()

    def _save_contract(self, contract_json):
        with open(self.contract_path, 'w', encoding="UTF-8") as contract_file:
            contract_file.write(json.dumps(contract_json,
                                           indent=4))
        self.contract_renderer.render_and_validate_contract(
            os.path.basename(self.contract_path)
        )

    def _check_request_kwargs(self, request_kwargs):
        if 'headers' not in request_kwargs:
            self._add_default_headers(request_kwargs)
        self._add_protocol_and_host(request_kwargs)

    @staticmethod
    def _add_default_headers(request_kwargs):
        request_kwargs['headers'] = "{{ config.default_headers }}"

    @staticmethod
    def _add_protocol_and_host(request_kwargs):
        uri = urlparse(request_kwargs['url'])
        if not uri.netloc:
            request_kwargs['url'] = "{{ config.host }}" + request_kwargs['url']
        if not uri.scheme:
            request_kwargs['url'] = "{{ config.protocol }}://" + request_kwargs['url']
        return request_kwargs
