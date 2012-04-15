# -*- coding: utf-8 -*-
#===============================================================================
# Name          : snmp
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : Class to define a standard Nagios SNMP plugin.
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

import logging as log
import os
import sys

from monitoring.nagios.plugin.base import NagiosPlugin
from monitoring.nagios.plugin.probes import ProbeSNMP

logger = log.getLogger('monitoring.nagios.plugin.snmp')

class NagiosPluginSNMP(NagiosPlugin):
    """Base for a standard SNMP Nagios plugin"""

    def __init__(self, name=os.path.basename(sys.argv[0]), version='', description=''):
        super(NagiosPluginSNMP, self).__init__(name, version, description)
        self.__probe = ProbeSNMP(
            hostaddress=self.options.hostname,
            community=self.options.snmpcommunity,
            snmpv2=self.options.snmpv2
        )

        if 'NagiosPluginSNMP' == self.__class__.__name__: logger.debug('=== END PLUGIN INIT ===')

    def define_plugin_arguments(self):
        """Define arguments for the plugin"""
        # Define common arguments
        super(NagiosPluginSNMP, self).define_plugin_arguments()
        
        # Add extra arguments
        self.required_args.add_argument('-C', dest='snmpcommunity', help='SNMP Community to use', required=True)
        self.parser.add_argument('-2', action='store_true', dest='snmpv2', default=False, help='Use SNMP v2c (default use version 1)')
        self.parser.add_argument('-p', type=int, dest='port', default=161, help='Port to connect to (default to 161).')

    def verify_plugin_arguments(self):
        """Check syntax of all arguments"""
        # Check common arguments syntax
        super(NagiosPluginSNMP, self).verify_plugin_arguments()
        
        if self.options.snmpv2:
            logger.debug('Using SNMP v2.')
            self.__use_snmp_v2 = 1

    def snmp_get(self, oid):
        """
        Query a SNMP OID using Get method.
        """
        return self.__probe.snmp_get(oid)

    def snmp_getnext(self, oid):
        """
        Query a SNMP OID using Getnext (walk) method.
        """
        return self.__probe.snmp_getnext(oid)