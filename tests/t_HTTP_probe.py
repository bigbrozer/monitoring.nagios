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

"""Test module for SSH based plugins."""

import unittest
import sys

from bs4 import BeautifulSoup

sys.path.insert(0, "..")
from monitoring.nagios.probes import ProbeHTTP


class TestHTTPProbe(unittest.TestCase):
    """Basic tests of HTTP probe functionalities."""
    def setUp(self):
        self.http = ProbeHTTP("monitoring-dc.app.corp")

    def test_instance_init(self):
        """Test instance initialization."""
        self.assertEqual(self.http.baseurl, "http://monitoring-dc.app.corp:80")

    def test_probe_auth(self):
        """Test HTTP probe auth."""
        http = ProbeHTTP("wwgrpapp0061.ww.corp", auth=('9nagios',
                                                       'PassNAD9@!@'))
        http_get_response = http.get("/")
        self.assertTrue(http_get_response.status_code == 200)

    def test_http_get(self):
        """Test HTTP GET request."""
        http_get_response = self.http.get("/")
        self.assertTrue(http_get_response.status_code == 200)

    def test_http_post(self):
        """Test HTTP POST request."""
        http = ProbeHTTP("httpbin.org")
        http_get_response = http.post("/post", data={"hello": "world"})
        self.assertTrue(http_get_response.status_code == 200)

    def test_bad_status_exception(self):
        """Test that HTTP request returns bad code."""
        with self.assertRaises(SystemExit):
            self.http.get("/rueyuzeytzeytiuytuez")

    def test_xml_parser_init(self):
        """Test fetching a XML file and parsing it."""
        http = ProbeHTTP("wweasapp0611.eas.ww.corp")
        response = http.get("/wweasapp0611.xml")
        self.assertIsInstance(response.xml(), BeautifulSoup)

    def test_xml_find_tag(self):
        """Test fetching a XML file and find a tag in it."""
        http = ProbeHTTP("wweasapp0611.eas.ww.corp")
        response = http.get("/wweasapp0611.xml")
        xml = response.xml()
        self.assertTrue(xml.alert.last_update)