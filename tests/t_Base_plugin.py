# -*- coding: utf-8 -*-
#===============================================================================
# Filename      : t_Base_plugin
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : Test Base plugin class.
#-------------------------------------------------------------------------------
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
#===============================================================================

import unittest
import os
import sys

from monitoring.nagios.plugin import NagiosPlugin

class TestBasePluginPickle(unittest.TestCase):
    """
    Test pickling data.
    """

    def setUp(self):
        sys.argv[1] = '-H'
        sys.argv[2] = 'monitoring-dc.app.corp'
        self.plugin = NagiosPlugin()
        self.delete_file(self.plugin.picklefile)

    def delete_file(self, file):
        try:
            os.remove(file)
        except OSError:
            pass

    def tearDown(self):
        self.delete_file(self.plugin.picklefile)

    def test_pickle_file_not_found(self):
        self.assertRaises(IOError, self.plugin.load_data)

    def test_pickle_save(self):
        l = [1, 2, 3, 4, 5]
        self.plugin.save_data(l)

    def test_pickle_load(self):
        l = [1, 2, 3, 4, 5]
        self.plugin.save_data(l)

        l = self.plugin.load_data()
        self.assertIn(4, l)

    def test_pickle_limit_record(self):
        l = []
        for i in range(0, 30):
            l.append(i)
        self.plugin.save_data(l, 10)
        l = self.plugin.load_data()
        self.assertEqual(10, len(l))

    def test_pickle_limit_continue(self):
        l = []
        for i in range(0, 30):
            l.append(i)
        self.plugin.save_data(l, 10)
        l = self.plugin.load_data()
        self.assertEqual(20, l[0])

