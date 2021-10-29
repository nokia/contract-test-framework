# Copyright 2021 Nokia
# Licensed under the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

from abc import ABCMeta, abstractmethod

from jsonschema import validate, ValidationError

from .contract_renderer import ContractRenderer
from .reporter import Reporter


class EndpointTester(metaclass=ABCMeta):
    """ Validates endpoints based on contracts

    Attributes:
        contract_dir (str): Path to directory of contracts to validate
        contract_renderer (object): Contract render module used to fill the Jinja2
            template of the contracts.
    """

    def __init__(self, contract_dir: str):
        self.contract_dir = contract_dir
        self.contract_renderer = ContractRenderer(contract_dir)
        self._reporter = None

    def make_requests_and_validates(self) -> None:
        """
        Functions goes through contracts in contract directory. For each contract
        a request is made corresponding to the request portion in the contract.
        The response is validated against json schema portion of the contract.
        A report gets printed to the shell
        """
        with Reporter().marginals() as self._reporter:
            contracts = self.contract_renderer.get_contracts(self.contract_dir)
            for contract in contracts:
                json_response = self._make_request(contract.content)
                self._validate(json_response, contract)
            self._check_result()

    @abstractmethod
    def _make_request(self, contract_json: dict) -> dict:
        """Makes a request based on the request specified in the contract json

        Uses the parameters from the request section in the contract
        Args:
            contract_json (dict): Dictionary based on the json from the contract
        Returns:
            dict: Json response received from the request in contract_json
        """

    def _validate(self, response_json, contract):
        try:
            validate(response_json, contract.content)
            self._reporter.print_report_results(contract.title)
        except ValidationError as e:
            self._reporter.print_report_results(contract.title, e)

    def _check_result(self):
        if self._reporter.failed:
            raise EndpointTesterException(f"Validation failed for following contracts: "
                                          f"{self._reporter.failed}")


class EndpointTesterException(Exception):
    """Exception raised when contract validation fails"""
