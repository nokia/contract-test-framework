# Copyright 2021 Nokia
# Licensed under the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import pytest


def test_contracts(mocked_request,  # pylint: disable=unused-argument
                   contract_tester,
                   capsys):
    contract_tester.make_requests_and_validates()
    out, _ = capsys.readouterr()
    expected_message = 'example_contract.json Successfully validated'
    assert_message_in_stdout(expected_message, out)


def test_invalid_contracts(mocked_request,  # pylint: disable=unused-argument
                           contract_tester_invalid,
                           capsys):

    with pytest.raises(SystemExit) as exception:
        contract_tester_invalid.make_requests_and_validates()
    assert exception.type == SystemExit
    assert exception.value.code == 1

    out, _ = capsys.readouterr()
    not_existing_message = "failed with the following error" \
                           " 'not_existing' is a required property"
    assert_message_in_stdout(not_existing_message, out)

    invalid_type_message = "failed with the following error 1000 is not of type 'string'"
    assert_message_in_stdout(invalid_type_message, out)


def assert_message_in_stdout(message, stdout):
    assert message in stdout
