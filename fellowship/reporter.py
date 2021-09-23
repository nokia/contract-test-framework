# Copyright 2021 Nokia
# Licensed under the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import logging
from contextlib import contextmanager
from datetime import datetime
from typing import Generator


LOGGER = logging.getLogger(__name__)


class Reporter:
    """Reports test results of the contract testing.

    Attributes:
        total_tests (int): The total amount of tests conducted. Default value 0
        failed (list): A list of failed tests. Default value empty list
    """
    def __init__(self) -> None:
        self.total_tests = 0
        self.failed = []

    @contextmanager
    def marginals(self) -> Generator['Reporter', None, None]:
        """ Generator that prints header/footer, and yields a reporter instance

            The reporter instance can be used to print the report, with the function
            print_report_results

        Yields:
            Reporter: an instance of the reporter which can be used to print the result
                of test cases
        """
        self._print_header()
        try:
            yield self
        finally:
            self._print_footer()

    def print_report_results(self, contract_title: str,
                             exception: Exception = None) -> None:
        """
        Function is used to print the result of each contract to the cli

        Args:
            contract_title (str): The title of the contract used for logging
            exception (Exception): Exception raised when validating contract. Defaults
                to None when validation is successful
        """
        self.total_tests += 1
        if exception:
            self.failed.append(contract_title)
            LOGGER.info("%s failed with the following error %s", contract_title,
                        exception)
        else:
            LOGGER.info("%s Successfully validated", contract_title)

    def _print_header(self):
        LOGGER.info("Test run started at %s", self._get_timestamp())
        LOGGER.info("Results:")

    def _print_footer(self):
        LOGGER.info("Test run finished at %s", self._get_timestamp())
        if self.failed:
            for contract in self.failed:
                LOGGER.error("Contract validation failed for: %s", contract)
            LOGGER.error("Total result: %d / %d", self.total_tests-len(self.failed),
                         self.total_tests)
        else:
            LOGGER.info("All contracts passed :)")
        LOGGER.info("End of test run")

    @staticmethod
    def _get_timestamp():
        return str(datetime.now())
