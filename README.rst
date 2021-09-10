========================
contract-test-framework
========================



``contract-test-framework`` contains an implementation of contract testing in Python. Under the package name fellowship

How to use from console:

If you want to validate an REST API, run Fellowship in validate mode.
If your contracts follow the Jinja2 syntax, make sure that you give the path to config.yaml
in environment variable ``contract_test_config``. You can see examples of contracts and config at
`example_contract.json <https://github.com/nokia/contract-test-framework/blob/main/tests/contracts/>`_.
Request part of the contract specifies the endpoint to make the request to. While everything under properties defines
the JSON schema to validate against.
Fellowship validates these contracts against a meta-schema before it makes the request.
Example of how to run from console:

.. code-block:: bash

    $ fellowship validate path/to/contract_directory/

To generate a contract in console, run in generate mode, with the following syntax: fellowship generate path_of_the
contract_to_generate request_kwargs expected_json. Request_kwargs is the request as a dictionary, the dictionary can take
following parameters:


    * | url: can be given as a full url, or just the endpoint (/api/v1/test) it will then fill out the Jinja 2 syntax for you
      | {{ config.protocol }}://{{ config.host}}/api/v1/test, when validating protocol and config will be filled
      | from config.yaml

    * | headers: can be given as a dictonary {"Accept": "application/json"}, if left empty it will automatically fill as
      | {{ config.default_headers | jsonify }}.

    * data: The body of the request

The last expected argument is the expected json response from the Rest API. The contract will generate with only types
and required for all fields. If you want to validate the values, you need to fill the consts and enums manually.


.. code-block:: bash

    $ fellowship generate sample.json '{"url": "/test", "method": "GET"}' '{"json": "expected_response"}'

Features
--------

REST endpoint contract testing and contract rendering.

Future development plans includes to support gRPC and message-based communication

Installation
------------

``fellowship`` will be made available on PyPI. You can install using `pip <https://pip.pypa.io/en/stable/>`_:

.. code-block:: bash

    $ pip install fellowship


Running the Test Suite
----------------------

If you have ``tox`` installed (perhaps via ``pip install tox`` or your
package manager), running ``tox`` in the directory of your source
checkout will run ``fellowship``'s test suite.

Contributing
------------

See how to contribute in `CONTRIBUTING.rst <https://github.com/nokia/contract-test-framework/blob/main/CONTRIBUTING.rst>`_.

The code and the issues are hosted on `GitHub <https://github.com/nokia/contract-test-framework>`_.

The project is licensed under BSD-3-Clause `BSD-3-Clause <https://github.com/nokia/contract-test-framework/blob/main/LICENSE>`_.