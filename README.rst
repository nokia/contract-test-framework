========================
contract-test-framework
========================



``contract-test-framework`` contains an implementation of contract testing in Python. Under the package name fellowship

How to use from console:

If you want to test contracts run in the console in validation mode

.. code-block:: bash

    $ fellowship validation path/to/contract_directory/

To generate a contract in console run in generation mode


.. code-block:: bash

    $ fellowship generation sample.json '{"url": "/test", "method": "GET"}' '{"json": "expected_response"}'

Features
--------

Support for REST endpoints contract testing framework

Installation
------------

``fellowship`` will be made available on PyPI. You can install using `pip <https://pip.pypa.io/en/stable/>`_:

.. code-block:: bash

    $ pip install fellowship


Running the Test Suite
----------------------

If you have ``tox`` installed (perhaps via ``pip install tox`` or your
package manager), running ``tox`` in the directory of your source
checkout will run ``contract-test-framework``'s test suite.

CONTRIBUTING
------------

To contribute to the project you can open a pull request related to one of the issues in project

The code and the issues are hosted on `GitHub <https://github.com/nokia/contract-test-framework>`_.

The project is licensed under BSD-3-Clause `BSD-3-Clause <https://github.com/nokia/contract-test-framework/blob/main/LICENSE>`_.