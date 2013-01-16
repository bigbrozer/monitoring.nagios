# -*- coding: utf-8 -*-
#===============================================================================
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : Test WMI plugin class.
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

from monitoring.nagios.plugin import NagiosPluginWMI


class TestWMIPlugin(unittest.TestCase):
    """
    Test WMI plugin class.
    """

    def setUp(self):
        sys.argv= sys.argv[:1]
        args = [
            '-H', '10.20.104.223',
            '-l', '9NagiosDC',
            '-p', 'NglP(23M,n',
            '-d', 'corp',
        ]
        sys.argv.extend(args)
        self.plugin = NagiosPluginWMI()

    def test_get_hostname(self):
        result = self.plugin.execute('SELECT * FROM Win32_OperatingSystem')
        self.assertEqual(result[0]['CSName'], 'WWGRPCTS6401')
