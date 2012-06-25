# -*- coding: utf-8 -*-
#===============================================================================
# Filename      : t_MSSQL_plugin
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : Test MSSQL plugin class.
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
import sys

from monitoring.nagios.plugin import NagiosPluginMSSQL


class TestMSSQLPlugin(unittest.TestCase):
    """
    Test MSSQL plugin class.
    """

    def setUp(self):
        #-H frselind0023.sel.fr.corp -u monitoring -p monitoring -d gIMM
        sys.argv[1] = '-H'
        sys.argv[2] = 'frselind0023.sel.fr.corp'
        sys.argv[3] = '-u'
        sys.argv[4] = 'monitoring'
        sys.argv[5] = '-p'
        sys.argv[6] = 'monitoring'
        sys.argv[7] = '-d'
        sys.argv[8] = 'gIMM'
        self.plugin = NagiosPluginMSSQL()

    def tearDown(self):
        self.plugin.close()

    def test_db_connection(self):
        self.assertTrue(self.plugin)

    def test_get_db_size(self):
        db_size = self.plugin.get_db_size()
        self.assertTrue('gIMM.Data' in db_size.keys())
