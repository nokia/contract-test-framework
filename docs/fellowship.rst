fellowship package
==================


Submodules
----------


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
   :show-inheritance:

fellowship.contract\_generator module
-------------------------------------

Usage example:

>>> import logging
>>> from fellowship.contract_generator import ContractGenerator
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
   :show-inheritance:


fellowship.reporter module
--------------------------

.. automodule:: fellowship.reporter
   :members:
   :undoc-members:
   :show-inheritance:

fellowship.contract module
--------------------------

.. automodule:: fellowship.contract
   :members:
   :undoc-members:
   :show-inheritance:

fellowship.utilis module
------------------------

.. automodule:: fellowship.utilis
   :members:
   :undoc-members:
   :show-inheritance:

Module contents
---------------

.. automodule:: fellowship
   :members:
   :undoc-members:
   :show-inheritance:
