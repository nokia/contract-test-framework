# Copyright 2021 Nokia
# Licensed under the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import sys
from contextlib import contextmanager
from datetime import datetime
from typing import Generator


class Reporter:
    """Reports test results of the contract testing.

    Attributes:
        total_tests (int): The total amount of tests conducted
        failed (list): A list of failed tests
    """
    def __init__(self) -> None:
        self.total_tests = 0
        self.failed = []

    @contextmanager
    def marginals(self) -> Generator['Reporter', None, None]:
        """ Generator that prints header, and generates a reporter instance which can be
            used for printing. Footer is printed after reporter is closed

        Yields:
            Reporter: an instance of the reporter which can be used to print the result
                of testcases

        Examples should be written in doctest format, and should illustrate how
        to use the function.

        >>> with Reporter().marginals() as r:
        >>>     r.print_report_results("test.json")
        """
        self._print_header()
        try:
            yield self
        finally:
            self._print_footer()

    def print_report_results(self, contract: str, exception: Exception = None) -> None:
        """
        Function is used to print the result of each contract to the cli
        """
        self.total_tests += 1
        if exception:
            self.failed.append(contract)
            print(f"{contract} failed with the following error {exception}")
        else:
            print(f"{contract} Successfully validated")

    def _print_header(self):
        print(f"Test run started at {self._get_timestamp()}")
        print("Results:")

    def _print_footer(self):
        print(f"Test run finished at {self._get_timestamp()}")
        if self.failed:
            for contract in self.failed:
                print(f"Contract validation failed for: {contract}")
            print(f"Total result: {self.total_tests-len(self.failed)} / "
                  f"{self.total_tests}")
            sys.exit(1)
        else:
            print("All contracts passed :)")
        print("End of test run")

    @staticmethod
    def _get_timestamp():
        return str(datetime.now())
