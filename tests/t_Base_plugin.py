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

"""Testing module for Base class plugin."""

import unittest
import os
import sys

sys.path.insert(0, "..")
from monitoring.nagios.plugin import NagiosPlugin


class PluginCustom(NagiosPlugin):
    """Custom plugin for tests."""
    def initialize(self):
        super(PluginCustom, self).initialize()
        self.toto = 'youpie'

    def define_plugin_arguments(self):
        super(PluginCustom, self).define_plugin_arguments()
        self.parser.add_argument('-t', action='store_true', dest='toto')

    def verify_plugin_arguments(self):
        super(PluginCustom, self).verify_plugin_arguments()
        if self.options.toto:
            self.toto = 'yourah'


class TestBasePluginPickle(unittest.TestCase):
    """
    Test pickling data.
    """

    def setUp(self):
        sys.argv = sys.argv[:1]
        args = [
            '-H', 'monitoring-dc.app.corp',
        ]
        sys.argv.extend(args)

        self.plugin = NagiosPlugin()
        self.delete_file(self.plugin.picklefile)

    def delete_file(self, filename):
        try:
            os.remove(filename)
        except OSError:
            pass

    def tearDown(self):
        self.delete_file(self.plugin.picklefile)

    def test_pickle_file_not_found(self):
        """Test case when pickle file cannot be found."""
        self.assertRaises(IOError, self.plugin.load_data)

    def test_pickle_save(self):
        """Test saving to pickle file."""
        l = [1, 2, 3, 4, 5]
        self.plugin.save_data(l)

    def test_pickle_load(self):
        """Test loading of pickled data."""
        l = [1, 2, 3, 4, 5]
        self.plugin.save_data(l)

        l = self.plugin.load_data()
        self.assertIn(4, l)

    def test_pickle_limit_record(self):
        """Test limiting number of records in pickle file."""
        l = []
        for i in range(0, 30):
            l.append(i)
        self.plugin.save_data(l, 10)
        l = self.plugin.load_data()
        self.assertEqual(10, len(l))

    def test_pickle_limit_continue(self):
        """Test continuation after loading next pickle data on next run."""
        l = []
        for i in range(0, 30):
            l.append(i)
        self.plugin.save_data(l, 10)
        l = self.plugin.load_data()
        self.assertEqual(20, l[0])


class TestBasePlugin(unittest.TestCase):
    """Test base plugin class."""
    def setUp(self):
        sys.argv = sys.argv[:1]
        args = [
            '-H', 'monitoring-dc.app.corp',
        ]
        sys.argv.extend(args)

        self.plugin = NagiosPlugin()

    def tearDown(self):
        try:
            del sys.argv[3]
        except IndexError:
            pass

    def test_plugin_initialize(self):
        """Test base plugin initialization."""
        p = PluginCustom()
        self.assertEqual('youpie', p.toto)

    def test_plugin_initialize_from_args(self):
        """Test base plugin argument processing."""
        sys.argv.append('-t')
        p = PluginCustom()
        self.assertEqual('yourah', p.toto)

    def test_arguments_parser(self):
        """Test base plugin argument value getter."""
        self.assertEqual('monitoring-dc.app.corp',
                         self.plugin.options.hostname)
