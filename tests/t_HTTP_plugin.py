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

"""Test module for HTTP based plugins."""

import unittest
import sys

from bs4 import BeautifulSoup

sys.path.insert(0, "..")
from monitoring.nagios.plugin import NagiosPluginHTTP


class TestHTTPPlugin(unittest.TestCase):
    """
    Test HTTP plugin class.
    """

    def setUp(self):
        sys.argv = sys.argv[:1]
        args = ['-H', 'monitoring-dc.app.corp']
        sys.argv.extend(args)
        self.plugin = NagiosPluginHTTP()

    def test_default_get(self):
        """Test that NagiosPluginHTTP is working well by default."""
        response = self.plugin.http.get(self.plugin.options.path)
        self.assertEqual(response.status_code, 200)