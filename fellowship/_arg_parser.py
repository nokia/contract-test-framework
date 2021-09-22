import argparse
import json

from .contract_generator import ContractGenerator
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
                    'invalid, fellowship raises system exit 1 at the end of the run. '
    )
    parser_validation.add_argument('path',
                                   type=str,
                                   help='The path to contract directory, that contains '
                                        'the contracts that should be validated')
    parser_validation.set_defaults(func=_validate)

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
             'While fields: data, headers and params are optional')
    parser_generation.add_argument(
        'expected_json',
        type=json.loads,
        help='An example of the expected json response to the request '
             'kwargs provided. This is used for generating the contract, '
             'the values of the fields will not matter. Since the '
             'contract will by default only validate the existence and '
             'type of the fields')
    parser_generation.set_defaults(func=_generate)
    return parser


def _validate(args):
    rest_tester = RestTester(args.path)
    rest_tester.make_requests_and_validates()


def _generate(args):
    contract_generator = ContractGenerator(args.path)
    contract_generator.generate_and_save_contract(request_kwargs=args.request_kwargs,
                                                  expected_json=args.expected_json)
