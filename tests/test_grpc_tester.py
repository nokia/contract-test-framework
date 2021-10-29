# Copyright 2021 Nokia
# Licensed under the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import logging


def test_contracts(grpc_contract_tester,
                   caplog,
                   mocker):
    caplog.set_level(logging.DEBUG)
    json_response = {"message": "Hello World!",
                     "personsSayingHello": {
                         "age": 64,
                         "name": "Bob"
                     }}
    mocker.patch.object(grpc_contract_tester,
                        "_make_request",
                        return_value=json_response)
    grpc_contract_tester.make_requests_and_validates()

    expected_message = 'grpc_reflection_contract.json Successfully validated'
    assert_message_in_stdout(expected_message, caplog.text)


def assert_message_in_stdout(message, caplog_messages):
    assert message in caplog_messages
