# Copyright 2021 Nokia
# Licensed under the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import os


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def test_grpc_generation(grpc_contract_generator):
    grpc_contract_generator.generate_grpc_contracts()
