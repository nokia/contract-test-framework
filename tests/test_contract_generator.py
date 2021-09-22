# Copyright 2021 Nokia
# Licensed under the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import json
import os


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def test_generation(contract_generator, request_dict, json_response, tmpdir):
    contract_generator.generate_and_save_contract(request_dict, json_response)
    generated_json = os.path.join(tmpdir, "test_contract.json")
    expected_json = os.path.join(CURRENT_DIR, "contracts", "example_contract.json")
    with open(generated_json, encoding="UTF-8") as file1, \
         open(expected_json, encoding="UTF-8") as file2:
        assert json.load(file1) == json.load(file2)
