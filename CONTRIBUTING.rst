How to contribute
=================

Contributing to fellowship is more than welcome. We want to keep it as
easy as possible to contribute changes that get things working in your
environment. There are a few guidelines that we need contributors to follow so that
we can have a chance of keeping on top of things.

Getting Started
---------------

-  Make sure you have a `GitHub account <https://github.com/join>`__.
-  Submit a Github ticket for your issue if one does not already exist.

   -  Clearly describe the issue including steps to reproduce if it is a
      bug.
   -  Include information from your environment.
   -  Make sure you fill in the earliest version that you know has the
      issue.

-  Fork the repository on GitHub.

Making Changes
--------------

-  Create a topic branch from master branch.

   - | To quickly create a topic branch based on main, run ``git checkout -b fix/main/my_contribution``.
     | Please avoid working directly on the ``main`` branch.
-  Make commits of logical and atomic units.
-  Check for unnecessary whitespace with ``git diff --check`` before committing.
-  | Make sure your commit messages are in the proper format. Start commit message with the issue number in brackets e.g.
   | [#1] for issue number 1.
-  Always run the tox tests before making a PR to ensure that the code follows quality and style requirements.
-  If the commit implements new functionality, makes sure to implement tests for this functionality as well.
-  See
   `ReadMe <https://https://github.com/nokia/contract-test-framework/blob/main/README.rst>`__
   for details how to run the tests

Submitting Changes
------------------

-  Push your changes to a topic branch in your fork of the repository.
-  Submit a pull request to the repository in the Nokia organization.
-  The core team looks at pull requests and comments on it

