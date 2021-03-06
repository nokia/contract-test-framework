fellowship package
==================

Module contents
---------------

.. automodule:: fellowship
   :members:
   :undoc-members:


fellowship.rest\_tester module
------------------------------

Usage example:

>>> from fellowship.rest_tester import RestTester
>>> rest_tester = RestTester(path_to_contract_directory)
>>> rest_tester.make_requests_and_validates()
Will print report that shows contracts that validation failed for, validation is
lazy so all contracts will be validated before result is shown.
If you would like more information about the validation set the logging level
to info. Example report:
ERROR    fellowship.reporter:reporter.py:69 Contract validation failed for:
/invalid_contracts/contract_wrong_type.json
ERROR    fellowship.reporter:reporter.py:69 Contract validation failed for:
/invalid_contracts/contract_missing_required.json
ERROR    fellowship.reporter:reporter.py:70 Total result: 0 / 2

.. automodule:: fellowship.rest_tester
   :members:
   :undoc-members:

fellowship.contract\_generator module
-------------------------------------

Usage example:

>>> import logging
>>> from fellowship.rest_contract_generator import ContractGenerator
>>> logging.basicConfig(level=logging.INFO)
>>> path_to_contract = os.path.join("contracts", "test_contract.json")
>>> request_kwargs = {"url": "/test?id=123","method": "GET"}
>>> expected_json = {"name": "Bob", "age": 72, "id": 123}
>>> contract_generator = ContractGenerator(path_to_contract)
>>> contract_generator.generate_and_save_contract(request_kwargs, expected_json)
The example output:
INFO:fellowship.contract_generator:The generated schema: {
    "$schema": "http://json-schema.org/schema#",
    "request": {
        "url": "{{ config.protocol }}://{{ config.host }}/test?id=123",
        "method": "GET",
        "headers": "{{ config.default_headers }}"
    },
    "type": "object",
    "properties": {
        "name": {
            "type": "string"
        },
        "age": {
            "type": "integer"
        },
        "id": {
            "type": "integer"
        }
    },
    "required": [
        "age",
        "id",
        "name"
    ]
}
Saved to file: test.json

.. automodule:: fellowship.contract_generator
   :members:
   :undoc-members:

fellowship.grpc\_tester module
------------------------------

Usage example:

>>> from fellowship.rest_tester import GrpcTester
>>> grpc_tester = GrpcTester(args.path)
>>> grpc_tester.make_requests_and_validates()
Will print report that shows contracts that validation failed for, validation is
lazy so all contracts will be validated before result is shown.
If you would like more information about the validation set the logging level
to info. Example report:
ERROR    fellowship.reporter:reporter.py:69 Contract validation failed for:
/invalid_contracts/contract_wrong_type.json
ERROR    fellowship.reporter:reporter.py:69 Contract validation failed for:
/invalid_contracts/contract_missing_required.json
ERROR    fellowship.reporter:reporter.py:70 Total result: 0 / 2

.. automodule:: fellowship.grpc_tester
   :members:
   :undoc-members:

fellowship.grpc\_generator module
---------------------------------

Usage example:

>>> from fellowship.grpc_generator import GrpcGenerator
>>> grpc_generator = GrpcGenerator(path_to_protofile, output_dir)
>>> grpc_generator.generate_grpc_contracts()

.. automodule:: fellowship.grpc_generator
   :members:
   :undoc-members:

fellowship.endpoint\_tester module
----------------------------------

.. automodule:: fellowship.endpoint_tester
   :members:
   :undoc-members:

fellowship.reporter module
--------------------------

.. automodule:: fellowship.reporter
   :members:
   :undoc-members:

fellowship.contract module
--------------------------

.. automodule:: fellowship.contract
   :members:
   :undoc-members:

fellowship.utilis module
------------------------

.. automodule:: fellowship.utilis
   :members:
   :undoc-members:
