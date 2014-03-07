#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Copyright (C) Vincent BESANCON <besancon.vincent@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""Setuptools configuration for this project."""

from setuptools import setup, find_packages

# Package dependencies
dependencies = [
    'pysnmp==4.2.4',
    'ssh==1.8.0',
    'pymssql==2.0.1',
    'requests==2.2.1',
    'beautifulsoup4==4.3.2',
]

# Way to obtain the project version if project is already installed somewhere
# in the Python path.
project_namespace = {}
with open("monitoring/nagios/__init__.py") as version_file:
    exec(version_file.read(), project_namespace)

# Init distribution
setup(
    name='monitoring.nagios',
    version=project_namespace["__version__"],
    description='Nagios plugin creation framework',
    author='Vincent BESANCON',
    author_email='besancon.vincent@gmail.com',
    license='MIT',
    namespace_packages=['monitoring'],
    packages=find_packages(),
    install_requires=dependencies
)
