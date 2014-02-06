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

"""Test module for WMI based plugins."""

import unittest
import sys

sys.path.insert(0, "..")
from monitoring.nagios.plugin import NagiosPluginWMI


class TestWMIPlugin(unittest.TestCase):
    """Test WMI plugin class."""
    def setUp(self):
        sys.argv = sys.argv[:1]
        args = [
            '-H', '10.20.104.223',
            '-l', '9NagiosDC',
            '-p', 'NglP(23M,n',
            '-d', 'corp',
        ]
        sys.argv.extend(args)
        self.plugin = NagiosPluginWMI()

    def test_get_hostname(self):
        """Test retrieving host name using WMI."""
        result = self.plugin.execute('SELECT * FROM Win32_OperatingSystem')
        self.assertEqual(result[0]['CSName'], 'WWGRPCTS6401')
