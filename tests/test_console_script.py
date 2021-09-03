# Copyright 2021 Nokia
# Licensed under the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import json
import os


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def test_validation(script_runner,
                    mocked_request):  # pylint: disable=unused-argument
    contract_dir = os.path.join(CURRENT_DIR, 'contracts/')
    ret = script_runner.run('contractor', 'validation', contract_dir)
    assert ret.success
    assert 'example_contract.json Successfully validated' in ret.stdout
    assert ret.stderr == ''


def test_generation(script_runner,
                    request_dict,
                    json_response,
                    tmpdir):
    ret = script_runner.run('contractor',
                            'generation',
                            os.path.join(tmpdir, 'test.json'),
                            json.dumps(request_dict),
                            json.dumps(json_response))
    assert ret.success
    assert f'Saved to file: {os.path.join(tmpdir, "test.json")}\n' in ret.stdout
    assert ret.stderr == ''
