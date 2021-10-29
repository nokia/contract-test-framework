# Copyright 2021 Nokia
# Licensed under the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import logging
import json
import os


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def test_grpc_generation(grpc_contract_generator,
                         caplog,
                         tmpdir):
    caplog.set_level(logging.DEBUG)
    grpc_contract_generator.generate_grpc_contracts()
    json_file = CURRENT_DIR + "/contracts/grpc/protos/test_HelloWorld_Send.json"
    generated_json = os.path.join(tmpdir, "test_HelloWorld_Send.json")
    with open(generated_json, encoding="UTF-8") as file1, \
            open(json_file, encoding="UTF-8") as file2:
        assert json.load(file1) == json.load(file2)
