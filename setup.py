#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#==============================================================================
# Module        : setup
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : Setuptools install script.
#------------------------------------------------------------------------------
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#==============================================================================

import os
from setuptools import setup, find_packages

# Package dependencies
dependencies = [
    'pysnmp==4.2.4',
    'ssh==1.8.0',
    'pymssql==2.0.1',
]


# Init distribute
setup(name='monitoring.nagios',
      version="1.2.5",
      description='Monitoring Python Package',
      author='Vincent BESANCON',
      author_email='besancon.vincent@gmail.com',
      license='GPL',
      namespace_packages=['monitoring'],
      packages=find_packages(),
      install_requires=dependencies,
      extras_require={'graph': ['pygraphviz>=1.0,<=1.1']})
