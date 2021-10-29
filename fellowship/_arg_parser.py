# Copyright 2021 Nokia
# Licensed under the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import argparse
import json

from .contract_generator import ContractGenerator
from .grpc_generator import GrpcGenerator
from .grpc_tester import GrpcTester
from .rest_tester import RestTester


def get_parser():
    parser = argparse.ArgumentParser(description='Contract tester based on json schema')
    subparsers = parser.add_subparsers()
    parser_validation = subparsers.add_parser(
        'validate',
        description='Validate command runs validation of contracts, by iterating over '
                    'the contracts located in the directory passed by the path arg. '
                    'During execution, fellowship prints a report to the command '
                    'line displaying the result.  If the validation of any contract is '
                    'invalid, fellowship raises RestTesterException at the end of the '
                    'run.'
    )
    parser_validation.add_argument('path',
                                   type=str,
                                   help='The path to contract directory, that contains '
                                        'the contracts that should be validated')
    parser_validation.set_defaults(func=_validate)

    parser_grpc_validation = subparsers.add_parser(
        'validate_grpc',
        description='Validate command runs validation of contracts, by iterating over '
                    'the contracts located in the directory passed by the path arg. '
                    'During execution, fellowship prints a report to the command '
                    'line displaying the result.  If the validation of any contract is '
                    'invalid, fellowship raises RestTesterException at the end of the '
                    'run.'
    )
    parser_grpc_validation.add_argument(
        'path',
        type=str,
        help='The path to contract directory, that contains the contracts that should '
             'be validated'
    )
    parser_grpc_validation.set_defaults(func=_validate_grpc)

    parser_generation = subparsers.add_parser(
        'generate',
        description='Generates a Rest contract based on request_kwargs and expected_json'
                    ' at the path given.'
    )
    parser_generation.add_argument('path',
                                   type=str,
                                   help='The path to were the new contract will '
                                        'be generated')
    parser_generation.add_argument(
        'request_kwargs',
        type=json.loads,
        help='A dictionary that contains the request kwargs to generate a '
             'new contract. Fields: url, method are required. '
             'While fields: data, headers and params are optional'
    )
    parser_generation.add_argument(
        'expected_json',
        type=json.loads,
        help='An example of the expected json response to the request '
             'kwargs provided. This is used for generating the contract, '
             'the values of the fields will not matter. Since the '
             'contract will by default only validate the existence and '
             'type of the fields'
    )
    parser_generation.add_argument(
        '-s', '--strict',
        action='store_true',
        help='Set flag when running generation in strict mode. Strict mode will generate'
             ' contract with expected value for each field.'
    )
    parser_generation.set_defaults(func=_generate)

    parser_grpc_generation = subparsers.add_parser(
        'generate_grpc',
        description='Generates all gRPC contract based on a proto file to the directory '
                    'given in path argument. Contracts name will consist of package '
                    'endpoint function.'
    )
    parser_grpc_generation.add_argument(
        'path',
        type=str,
        help='The output directory to store the gRPC contracts generated'
    )
    parser_grpc_generation.add_argument(
        'proto_file',
        type=str,
        help='The proto that generation will be based on. Generates contracts for all '
             'endpoints, one contract per function.'
    )
    parser_grpc_generation.set_defaults(func=_grpc_generate)

    return parser


def _validate(args):
    rest_tester = RestTester(args.path)
    rest_tester.make_requests_and_validates()


def _validate_grpc(args):
    grpc_tester = GrpcTester(args.path)
    grpc_tester.make_requests_and_validates()


def _generate(args):
    contract_generator = ContractGenerator(args.path)
    if args.strict:
        contract_generator.set_type_of_schema_builder("strict")
    contract_generator.generate_and_save_contract(request_kwargs=args.request_kwargs,
                                                  expected_json=args.expected_json)


def _grpc_generate(args):
    grpc_generator = GrpcGenerator(args.proto_file, args.path)
    grpc_generator.generate_grpc_contracts()
