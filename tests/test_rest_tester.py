# Copyright 2021 Nokia
# Licensed under the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import logging
import pytest

from fellowship.rest_tester import RestTesterException


@pytest.mark.usefixtures("mocked_request")
def test_contracts(contract_tester,
                   caplog):
    caplog.set_level(logging.DEBUG)
    contract_tester.make_requests_and_validates()
    expected_message = 'example_contract.json Successfully validated'
    assert_message_in_stdout(expected_message, caplog.text)


@pytest.mark.usefixtures("mocked_request")
def test_invalid_contracts(contract_tester_invalid,
                           caplog):
    caplog.set_level(logging.DEBUG)
    with pytest.raises(RestTesterException) as exception:
        contract_tester_invalid.make_requests_and_validates()
    assert "Validation failed for following contracts" in str(exception)

    not_existing_message = "failed with the following error" \
                           " 'not_existing' is a required property"
    assert_message_in_stdout(not_existing_message, caplog.text)

    invalid_type_message = "failed with the following error 1000 is not of type 'string'"
    assert_message_in_stdout(invalid_type_message, caplog.text)


def assert_message_in_stdout(message, caplog_messages):
    assert message in caplog_messages
