# Copyright 2021 Nokia
# Licensed under the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import json

import requests

from .endpoint_tester import EndpointTester


class RestTester(EndpointTester):
    """Validates Rest endpoints based on contracts. Inherits EndpointTester
    """
    _requests_arg_names = ['headers', 'data', 'params']

    def _make_request(self, contract_json):
        request_kwargs = self._construct_request_kwargs(contract_json)
        return requests.request(method=contract_json['request']['method'],
                                url=contract_json['request']['url'],
                                **request_kwargs).json()

    def _construct_request_kwargs(self, contract_json):
        request_kwargs = {kwarg: contract_json['request'][kwarg]
                          for kwarg in self._requests_arg_names
                          if kwarg in contract_json['request']}

        if 'data' in request_kwargs:
            request_kwargs['data'] = json.dumps(request_kwargs['data'])
        return request_kwargs


class RestTesterException(Exception):
    """Exception raised when contract validation fails"""
