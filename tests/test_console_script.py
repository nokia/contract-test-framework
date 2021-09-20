# Copyright 2021 Nokia
# Licensed under the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

# pylint: disable=protected-access

import json
import sys
import types
import os

import pytest

from fixed_load_script import fixed_load_script


# TODO: Follow up if this is fixed in pytest_console_script. Link to repo and PR can be
# found in fixed_load_script.py. Actions:
# Remove the associated decorators, @pytest.mark.usefixtures("fix_script_runner").
# Remove pylint disable # pylint: disable=protected-access
@pytest.fixture
def fix_script_runner(script_runner):
    script_runner._load_script = types.MethodType(fixed_load_script, script_runner)


@pytest.fixture(autouse=True)
def clean_fellowship_from_modules_cache():
    for m in sys.modules.copy():
        if "fellowship" in m:
            del sys.modules[m]


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


@pytest.mark.usefixtures("fix_script_runner")
@pytest.mark.usefixtures("mocked_request")
def test_validation(script_runner):
    contract_dir = os.path.join(CURRENT_DIR, 'contracts/')
    ret = script_runner.run('fellowship', 'validate', contract_dir)
    assert ret.success
    assert 'example_contract.json Successfully validated' in ret.stderr


@pytest.mark.usefixtures("fix_script_runner")
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
    assert f'Saved to file: {os.path.join(tmpdir, "test.json")}\n' in ret.stderr
