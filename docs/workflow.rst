Example workflow
================

Examples on how Fellowship could be used for contract generation and validation.

Rest Contract Generation
------------------------

.. graphviz::

 digraph {
      rankdir=TB
      label="Example workflow to generate contract";
      node [style=filled]
      subgraph sequence {
         node [shape=circle, color=lightblue, width=1.5 height=1.5];
         start [label="Start"];
         stop  [label="Ready for validation"];
         node [shape=box, color=lightblue, width=1 height=1];
         define [label="1. Define the request"];
         acquire [label="2. Acquire Expected Json"];
         node [shape=box, color=lightcoral, width=1 height=1];
         generate [label="3. Generate Contract"];
         node [shape=box, color=wheat];
         strictcontract [label="4. Strict or type\nverification?",
                         color=lightblue, shape=diamond,
                         width=1.5 height=1.5];
         node [shape=box, color=lightblue, width=1 height=1];
         tag [label="5. Add const and enum\nto the generated contract"];
         done [label="6. All contracts done?\n", color=lightblue, shape=diamond,
               width=1.5 height=1.5];
         start -> define -> acquire -> generate -> strictcontract
         strictcontract -> tag [label="strict"];
         strictcontract -> done [label="type"];
         tag -> done;
         done -> stop [label="yes"];
         done -> define [label="no"];
         {rank=same; define; acquire; generate};
      }
      subgraph roles {
         node [shape=box]
         contributor [label="User", color=lightblue]
         ci [label="Fellowship", color=lightcoral]
         {rank=same; contributor}
      }
   }

1. Define request
^^^^^^^^^^^^^^^^^
First define the request that is used to access the target API.
This includes the endpoint, method and potentially body and header.
Header can also be dynamically filled in the validation phase.

2. Acquire expected JSON
^^^^^^^^^^^^^^^^^^^^^^^^
Acquire or create the expected json, you can do this, for example, by executing
the request against the target API or base it on your expectation of the API.

3. Generate contract
^^^^^^^^^^^^^^^^^^^^
Generate contract, by using fellowships generate command in the command-line.
Syntax is:

fellowship generate path_to_new_contract request_dict expected_json

4. Define type of contract
^^^^^^^^^^^^^^^^^^^^^^^^^^
Define if the validation is depending on the type of the field or the value of
the field. The automatically generated contract validates the field. If
Fellowship shall evaluate the value of the field, the contract needs further
modification.

5. Add field validation
^^^^^^^^^^^^^^^^^^^^^^^
If the value of the field is strict, add const to the fields that require to
strict validation. However, if the field can take several values, use enum
instead. In the enum field, you can give a list of all potential values and the
validation ensures that the enum contains the value of the response.
There are several other validators in Json Schema such as maximum, minimum refer
to `JSON Schema Reference
<https://json-schema.org/understanding-json-schema/reference/generic.html>`_
for more information.

6. Are all endpoints covered?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If the coverage of endpoints is complete, you are ready to move to validation.
Otherwise, repeat from step 1 until you reach satisfaction with the coverage.


Example Rest Contract Validation Pipeline
-----------------------------------------

This is an example of how you can integrate fellowship into your testing
pipeline

.. graphviz::

 digraph {
      rankdir=TB
      label="Example pipeline to validate contracts";
      node [style=filled]
      subgraph sequence {
         node [shape=circle, color=lightblue width=2 height=2];
         start [label="Start"];
         stop  [label="Done"];
         node [shape=box, color=lightblue width=1.5 height=1.5];
         download [label="1. Get contracts from\ncontract repo"];
         launch [label="2. Launch target application\n"];
         jinja2 [label="3. Does contracts use\n jinja2 template?", color=lightblue, shape=diamond, width=2.5, height=2.5];
         node [shape=box, color=lightblue width=1.5 height=1.5];
         generate [label="4. Collect dynamic variables\nto config.yaml"];
         env [label="5. set env variable contract_test_config\n to config.yaml path"];
         node [shape=box, color=lightcoral];
         validate [label="6. Launch validation\n"];
         start -> download -> launch -> jinja2
         jinja2 -> validate [label="no"];
         jinja2 -> generate [label="yes"];
         generate -> env;
         env -> validate;
         validate -> stop;
         {rank=same; download; launch; jinja2};
      }
      subgraph roles {
         node [shape=box]
         contributor [label="Pipeline", color=lightblue]
         ci [label="Fellowship", color=lightcoral]
         {rank=same; contributor}
      }
   }


1. Get contracts from contract repo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Download the contracts from a remote repository. This is most common with
consumer driven contract testing. This is, of course, optional and if the
contracts are already inside the repository, you can skip this step.

2. Start the application
^^^^^^^^^^^^^^^^^^^^^^^^
Start the application so that it can respond to the Rest requests.

3. Does contracts use jinja2 template
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you made the contracts using the jinja2 template, then Fellowship will render
them at run time. This requires steps 4 and 5 to be performed.

4. Collect dynamic variables to config.yaml
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Collect variables such as host, protocol and headers, the pipeline fills these
in the config.yaml, so it can render the contracts. The config yaml can also be
pre-made if that is preferred. For an example of the config.yaml check the
default config.yaml. `rest_config.yaml
<https://github.com/nokia/contract-test-framework/blob/main/fellowship/
configs/rest_config.yaml>`_

5. Set env variable contract_test_config
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Fellowship access the config.yaml through the environment variable
contract_test_config, so you should set it to the config.yaml path.

6. Launch validation
^^^^^^^^^^^^^^^^^^^^
Now Fellowship is ready to validate the contracts, this is done by executing:

fellowship validate path_to_contract_directory
