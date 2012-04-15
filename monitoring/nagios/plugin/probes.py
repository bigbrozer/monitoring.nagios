# -*- coding: utf-8 -*-
#===============================================================================
# Name          : probes
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : Classes that provide a way to probe a host using SNMP, WMI,
#                 etc...
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

# TODO: Allow to use more OIDs in methods snmp_*().
# TODO: Rewrite methods snmp_*(), to much copy / paste.

from pprint import pformat
import logging as log
from pysnmp.entity.rfc3413.oneliner import cmdgen

from monitoring.nagios.plugin.exceptions import NagiosUnknown
logger = log.getLogger('monitoring.nagios.plugin.probes')

class Probe(object):
    """
    Class Probe.
    """
    def __init__(self, hostaddress='', port=None):
        logger.debug('')
        logger.debug('=== BEGIN NEW PROBE INIT ===')
        logger.debug('Instanciating a new probe of type %s.' % self.__class__.__name__)

        self._hostaddress = hostaddress
        self._port = port

        if 'Probe' == self.__class__.__name__: logger.debug('=== END PROBE INIT ===')

class ProbeSNMP(Probe):
    """
    Class ProbeSNMP.
    """
    def __init__(self, hostaddress='', port=161, community='public', snmpv2=False):
        super(ProbeSNMP, self).__init__(hostaddress, port)

        self._community = community
        self._snmpv2 = snmpv2

        logger.debug('Probe attributes:')
        logger.debug(pformat(vars(self), indent=4))

        if 'ProbeSNMP' == self.__class__.__name__: logger.debug('=== END PROBE INIT ===')

    # Public methods (the ones you should use ;-))
    def snmp_get(self, oid):
        """
        Query a SNMP OID using SNMP Get and return a tuple (oid, value).
        """
        logger.debug('')
        logger.debug('=== BEGIN SNMP GET QUERY ===')
        logger.debug('Query SNMP Get on host %s for OID %s.' % (self._hostaddress, oid))

        # Convert dotted OID notation to a tuple if it is a dotted notation string
        if type(oid) is str:
            oid = self.__convert_oid_to_tuple(oid)

        try:
            logger.debug('Establishing SNMP connection to \'%s:%d\' with community \'%s\' using SNMPv2 (%s)...' % (
                self._hostaddress,
                self._port,
                self._community,
                self._snmpv2)
            )
            errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(
                cmdgen.CommunityData('nagios-plugin', self._community, self._snmpv2),
                cmdgen.UdpTransportTarget((self._hostaddress, self._port)),
                oid
            )
        except Exception as e:
            raise NagiosUnknown('''Unexpected error during SNMP Get query !\nHost: %s\nCommunity: %s\nOID: %s\nMessage: %s''' % (
                self._hostaddress, self._community, oid, e))

        if errorIndication is not None: raise NagiosUnknown('SNMP query error: %s' % errorIndication)

        logger.debug('Returned Varbinds:')
        logger.debug(pformat(varBinds, indent=4))
        logger.debug('=== END SNMP QUERY ===')

        return varBinds.pop()

    def snmp_getnext(self, oid):
        """
        Query a SNMP OID using SNMP Getnext and return a list of tuples
        [(oid, value), (...), ...].
        """
        logger.debug('')
        logger.debug('=== BEGIN SNMP GETNEXT QUERY ===')
        logger.debug('Query SNMP Getnext on host %s for OID %s.' % (self._hostaddress, oid))

        # Convert dotted OID notation to a tuple if it is a dotted notation string
        if type(oid) is str:
            oid = self.__convert_oid_to_tuple(oid)

        try:
            logger.debug('Establishing SNMP connection to \'%s:%d\' with community \'%s\' using SNMPv2 (%s)...' % (
                self._hostaddress,
                self._port,
                self._community,
                self._snmpv2)
            )
            errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().nextCmd(
                cmdgen.CommunityData('nagios-plugin', self._community, self._snmpv2),
                cmdgen.UdpTransportTarget((self._hostaddress, self._port)),
                oid
            )
        except Exception as e:
            raise NagiosUnknown('''Unexpected error during SNMP Get query !\nHost: %s\nCommunity: %s\nOID: %s\nMessage: %s''' % (
                self._hostaddress, self._community, oid, e))

        if errorIndication is not None: raise NagiosUnknown('SNMP query error: %s' % errorIndication)

        logger.debug('Returned Varbinds:')
        logger.debug(pformat(varBinds, indent=4))
        logger.debug('=== END SNMP QUERY ===')

        values = []
        for varBind in varBinds:
            values.append(varBind[0][1])

        return values

    # Private methods for internal processing
    def __convert_oid_to_tuple(self, oid_str):
        logger.debug('-- Converting OID string to Tuple: %s' % oid_str)
        return tuple([int(chr) for chr in oid_str.split('.')])

    def __convert_tuple_to_oid(self, oid_tuple):
        logger.debug('-- Converting OID Tuple to string: %s' % oid_tuple)
        oid_str = [str(i) for i in oid_tuple]
        return ".".join(oid_str)

