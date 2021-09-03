# Copyright 2021 Nokia
# Licensed under the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import json
import os
import pytest
from fellowship.cli import parse_args


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture(name="args")
def fixture_args(request_dict, json_response, tmpdir):
    path = os.path.join(tmpdir, "test_contract.json")
    parser = parse_args(["generation",
                         path,
                         json.dumps(request_dict),
                         json.dumps(json_response)])
    return parser


def test_generation(contract_generator, args, tmpdir):
    contract_generator.generate_and_save_contract(args)
    generated_json = os.path.join(tmpdir, "test_contract.json")
    expected_json = os.path.join(CURRENT_DIR, "contracts", "example_contract.json")
    with open(generated_json, encoding="UTF-8") as file1, \
         open(expected_json, encoding="UTF-8") as file2:
        assert json.load(file1) == json.load(file2)
