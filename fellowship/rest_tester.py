# Copyright 2021 Nokia
# Licensed under the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import requests

from .endpoint_tester import EndpointTester


class RestTester(EndpointTester):
    """Validates Rest endpoints based on contracts
    Attributes:
        contract_dir (str): Path to directory of contracts to validate
        contract_renderer (object): Contract render module used to fill the Jinja2
            template of the contracts.
    """
    _requests_arg_names = ['headers', 'data', 'params']

    def _make_request(self, contract_json):
        request_kwargs = self._construct_request_kwargs(contract_json)
        return requests.request(method=contract_json['request']['method'],
                                url=contract_json['request']['url'],
                                **request_kwargs).json()


class RestTesterException(Exception):
    """Exception raised when contract validation fails"""
