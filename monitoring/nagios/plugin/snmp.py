# -*- coding: UTF-8 -*-
#
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

from monitoring.nagios.plugin.base import NagiosPlugin
from monitoring.utils.snmp import snmp_get, snmp_next

class NagiosPluginSNMP(NagiosPlugin):
    """Base for a standard SNMP Nagios plugin"""

    def __init__(self, name, version, description):
        super(NagiosPluginSNMP, self).__init__(name, version, description)
        self.usesnmpv2 = 0

    def define_plugin_arguments(self):
        """Define arguments for the plugin"""
        # Define common arguments
        super(NagiosPluginSNMP, self).define_plugin_arguments()
        
        # Add extra arguments
        self.parser.add_argument('-C', dest='snmpcommunity', help='SNMP Community to use', required=True)
        self.parser.add_argument('-2', action='store_true', dest='snmpv2', default=False, help='Use SNMP v2c (default use version 1)')

    def verify_plugin_arguments(self):
        """Check syntax of all arguments"""
        # Check common arguments syntax
        super(NagiosPluginSNMP, self).verify_plugin_arguments()
        
        if self.options.snmpv2:
            self.usesnmpv2 = 1

    def snmpget(self, oid_param):
        """
        Query a SNMP OID using Get method.
        """
        self.log.debug('SNMP Get on host %s for OID %s.' % (self.options.hostname, oid_param))
        return snmp_get(self.options.hostname, self.options.snmpcommunity, oid_param, snmpv2=self.options.snmpv2)

    def snmpnext(self, oid_param):
        """
        Query a SNMP OID using Next (walk) method.
        """
        self.log.debug('SNMP Next on host %s for OID %s.' % (self.options.hostname, oid_param))
        return snmp_next(self.options.hostname, self.options.snmpcommunity, oid_param, snmpv2=self.options.snmpv2)

if __name__ == '__main__':
    from monitoring.log import mainlog

    mainlog.info('Creating instance of the plugin.')
    plugin = NagiosPluginSNMP("helloSNMP", "1.0", "Just a SNMP test")
    mainlog.info('Done.')