# Copyright 2021 Nokia
# Licensed under the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import logging
import sys

from ._arg_parser import get_parser


logging.basicConfig(level=logging.INFO, stream=sys.stdout)


def parse_args(args):
    parser = get_parser()
    return parser.parse_args(args)


def run():
    parser = parse_args(sys.argv[1:])
    parser.func(parser)
