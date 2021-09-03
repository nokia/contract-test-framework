# Copyright 2021 Nokia
# Licensed under the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import os
from setuptools import Command, setup


THISDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
VERSION_FILE = os.path.join(THISDIR, 'fellowship', 'version.py')


def get_version():
    with open(VERSION_FILE) as ver:
        return ver.read().split('=')[1].strip().strip("'")


__version__ = get_version()


setup(name='fellowship',
      version=__version__,
      description='Library for testing api endpoints ',
      packages=['fellowship'],
      entry_points={
        'console_scripts': ['fellowship=fellowship.cli:run'],
      },
      package_data={
          '': ['schemas/*', 'configs/*']
      },
      author='Robin Nyman',
      author_email='robin.nyman@nokia.com',
      zip_safe=False)