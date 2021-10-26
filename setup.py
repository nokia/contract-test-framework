# Copyright 2021 Nokia
# Licensed under the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import os
from setuptools import setup


CURRENT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
VERSION_FILE = os.path.join(CURRENT_DIR, 'fellowship', '_version.py')
with open(VERSION_FILE) as ver:
    __version__ = ver.read().split('=')[1].strip().strip("'")


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(name='fellowship',
      version=__version__,
      description='Library for testing api endpoints ',
      packages=['fellowship'],
      install_requires=['Jinja2',
                        'attrs',
                        'genson',
                        'grpc-requests',
                        'grpcio',
                        'grpcio-tools',
                        'jsonschema',
                        'pyyaml',
                        'requests',
                        'rfc3987'],
      entry_points={
          'console_scripts': ['fellowship=fellowship.cli:run'],
      },
      package_data={
          '': ['schemas/*', 'configs/*']
      },
      author='Robin Nyman',
      author_email='robin.nyman@nokia.com',
      license='BSD-3-Clause',
      long_description=read('README.rst'),
      url='https://github.com/nokia/contract-test-framework',
      classifiers=['Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8',
                   'Programming Language :: Python :: 3.9',
                   'Topic :: Software Development :: Testing'],
      keywords="Microservice Contract Testing")
