# Copyright 2021 Nokia
# Licensed under the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import json
import os

import pytest


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


@pytest.mark.usefixtures("mocked_request")
def test_validation(script_runner):
    contract_dir = os.path.join(CURRENT_DIR, 'contracts/')
    ret = script_runner.run('fellowship', 'validate', contract_dir)
    assert ret.success
    assert 'example_contract.json Successfully validated' in ret.stdout
    assert ret.stderr == ''


def test_generation(script_runner,
                    request_dict,
                    json_response,
                    tmpdir):
    ret = script_runner.run('fellowship',
                            'generate',
                            os.path.join(tmpdir, 'test.json'),
                            json.dumps(request_dict),
                            json.dumps(json_response))
    assert ret.success
    assert f'Saved to file: {os.path.join(tmpdir, "test.json")}\n' in ret.stdout
    assert ret.stderr == ''
