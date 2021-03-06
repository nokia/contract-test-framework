# Copyright 2021 Nokia
# Licensed under the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import os

import pytest
import requests_mock

from fellowship.contract_generator import ContractGenerator
from fellowship.grpc_generator import GrpcGenerator
from fellowship.grpc_tester import GrpcTester
from fellowship.rest_tester import RestTester


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def grpc_contract_tester():
    contract_dir = os.path.join(CURRENT_DIR, "contracts", "grpc")
    return GrpcTester(contract_dir)


@pytest.fixture(name="protobuf_path")
def test_protobuf_path():
    return os.path.join(CURRENT_DIR, "contracts", "grpc", "protos", "test.proto")


@pytest.fixture
def grpc_contract_generator(protobuf_path, tmpdir):
    return GrpcGenerator(protobuf_path, tmpdir)


@pytest.fixture
def rest_contract_tester():
    contract_dir = os.path.join(CURRENT_DIR, "contracts")
    return RestTester(contract_dir)


@pytest.fixture
def rest_contract_tester_invalid():
    contract_dir = os.path.join(CURRENT_DIR, "invalid_contracts")
    return RestTester(contract_dir)


@pytest.fixture
def rest_contract_generator(tmpdir):
    path = os.path.join(tmpdir, "test_contract.json")
    return ContractGenerator(path)


@pytest.fixture(name="json_response")
def json_payload():
    return {"checked": True,
            "id": 1000,
            "name": "T-Rex",
            "price": 9.99,
            "tags": [["pre-historic", "blue", "plushy"]],
            "related_item": {
                "name": "Bear",
                "price": 12.25
                }
            }


@pytest.fixture
def request_dict():
    return {"url": "/test",
            "method": "POST",
            "headers": {
               "Content-Type": "application/json",
               "Accept": "application/json"
            },
            "data": {
                "value": "test"
            }}


@pytest.fixture(name="mock_request")
def mock_requests():
    with requests_mock.Mocker(case_sensitive=True) as m:
        yield m


@pytest.fixture
def mocked_request(json_response,
                   mock_request):
    response_list = [{'json': json_response, 'status_code': 200}]
    server_url = "http://localhost"
    mock_request.register_uri(
        'POST',
        server_url + "/test",
        complete_qs=True,
        response_list=response_list)
    return mock_request
