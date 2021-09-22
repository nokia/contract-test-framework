# Copyright 2021 Nokia
# Licensed under the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import attr


@attr.s(frozen=True)
class Contract:
    """ Class to save the contents of a contract and a title for it

    Attributes:
        title (str): Title of the contract
        content (dict): Json contents of the contract
    """
    title = attr.ib()
    content = attr.ib()
