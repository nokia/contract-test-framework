# Copyright 2021 Nokia
# Licensed under the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import json
import glob
import os

from jinja2 import Environment, FileSystemLoader

from .utilis import load_config, validate_contract
from .contract import Contract


class ContractRenderer:
    """Renders the json contract based on jinja2 template.
    Attributes:
        config (dict): Dictionary of configurations such as url and header
        jinja_env (object): Jinja environment used for rendering contracts
        jinja_env.filters['jsonify']: filter to automatically json dump to contract
    """

    config = load_config()

    def __init__(self, template_directory: str) -> None:
        self.jinja_env = Environment(loader=FileSystemLoader(template_directory))
        self.jinja_env.filters['jsonify'] = json.dumps

    def render_and_validate_contract(self, fname: str) -> dict:
        """Renders contracts from jinja2 template to json and validates them
        Args:
            fname (str): Name of the contract file to render and validate
        Returns:
            dict: A json dictionary
        """
        jinja_template = self.jinja_env.get_template(os.path.basename(fname))
        contract_dict = json.loads(jinja_template.render(config=self.config))
        validate_contract(contract_dict)
        return contract_dict

    def get_contracts(self, contract_dir: str) -> list:
        """Finds all contracts in directory, the contracts are also rendered and \
           validated
        Args:
            contract_dir: The path to the directory where the contracts are located
        Returns:
            list: A list of Contract objects
        """
        return list(self._contract_dicts(contract_dir))

    def _contract_dicts(self, contract_dir):
        for fname in glob.glob(os.path.join(contract_dir, '*.json')):
            contract_dict = self.render_and_validate_contract(fname)
            yield Contract(fname, contract_dict)
