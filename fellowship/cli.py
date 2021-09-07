# Copyright 2021 Nokia
# Licensed under the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import argparse
import json
import sys
from .contract_generator import ContractGenerator
from .rest_tester import RestTester


def parse_args(args):
    parser = argparse.ArgumentParser(description='Contract tester based on json schema')
    subparsers = parser.add_subparsers()
    parser_validation = subparsers.add_parser('validate')
    parser_validation.add_argument('path',
                                   type=str,
                                   help='The path to contract directory')
    parser_validation.set_defaults(func=validate)

    parser_generation = subparsers.add_parser('generate')
    parser_generation.add_argument('path',
                                   type=str,
                                   help='The path to were the new contract will '
                                        'be generated')
    parser_generation.add_argument(
        'request_kwargs',
        type=json.loads,
        help='A dictonary that contains the request kwargs to generate a '
        'new contract. Fields: url, method are required. '
        'While fields: data, headers and params are optional')
    parser_generation.add_argument(
        'expected_json',
        type=json.loads,
        help='An example of the expected json response to the request '
             'kwargs provided. This is used for generating the contract, '
             'the values of the fields will not matter. Since the '
             'contract will by default only validate the existence and '
             'type of the fields')
    parser_generation.set_defaults(func=generate)
    return parser.parse_args(args)


def validate(args):
    rest_tester = RestTester(args.path)
    rest_tester.make_requests_and_validates()


def generate(args):
    contract_generator = ContractGenerator(args.path)
    contract_generator.generate_and_save_contract(args)


def run():
    args = parse_args(sys.argv[1:])
    args.func(args)
