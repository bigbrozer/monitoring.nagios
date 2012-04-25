#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#===============================================================================
# Filename      : snmp_query.py
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : Test SNMPQuery class.
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

# TODO: Convert to unittest.

import sys

sys.path.insert(0, '..')

from monitoring.nagios.plugin import NagiosPluginSNMP
from monitoring.nagios.plugin.probes import ProbeSNMP

plugin = NagiosPluginSNMP(version='1.0', description='Test SNMPQuery class')

query_get = plugin.snmp.get({
    'name': '1.3.6.1.4.1.1588.2.1.1.1.6.2.1.36.65',
    'alias': '1.3.6.1.4.1.1588.2.1.1.1.6.2.1.37.65',
    'crc': '1.3.6.1.4.1.1588.2.1.1.1.6.2.1.22.65',
})
print query_get

print '=' * 80

query_getnext = plugin.snmp.getnext({
    'indexes': '1.3.6.1.4.1.1588.2.1.1.1.6.2.1.1',
    'alias': '1.3.6.1.4.1.1588.2.1.1.1.6.2.1.37',
})
print query_getnext

print '=' * 80

cisco_probe = ProbeSNMP('10.20.129.1', community='DmbmfubZ', snmpv2=True)
query_table = cisco_probe.table({
    'indexes': '1.3.6.1.4.1.9.9.109.1.1.1.1.2',
    'entity_name': '1.3.6.1.2.1.47.1.1.1.1.7',
    'cpu_usages': '1.3.6.1.4.1.9.9.109.1.1.1.1.8',
})
print query_table

print '=' * 80

query_san_table = plugin.snmp.table({
    'indexes': '1.3.6.1.4.1.1588.2.1.1.1.6.2.1.1',
    'name': '1.3.6.1.4.1.1588.2.1.1.1.6.2.1.36.65',
    'alias': '1.3.6.1.4.1.1588.2.1.1.1.6.2.1.37',
    'crc': '1.3.6.1.4.1.1588.2.1.1.1.6.2.1.22.65',
})
print query_san_table