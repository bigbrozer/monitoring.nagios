# -*- coding: utf-8 -*-
#===============================================================================
# Filename      : snmp
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : 
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

from pprint import pformat
import logging as log
from pysnmp.entity.rfc3413.oneliner import cmdgen

from monitoring.nagios.plugin.probes import Probe
from monitoring.nagios.plugin.exceptions import NagiosUnknown
from monitoring.nagios.plugin.utilities import find_key_from_value

logger = log.getLogger('monitoring.nagios.plugin.probes')


class SNMPQuery(object):
    """
    Class that construct a SNMP query.
    """

    def __init__(self, probe, oidstable, snmpcmd='get'):
        self.__probe = probe
        self.__oids = oidstable
        self.__snmpcmd = snmpcmd

    def __get_raw_oid_values(self, oid):
        """
                    Launch a SNMP query on a OID, return raw data as a list.
                    """

        logger.debug('-- Probe OID: %s ...' % oid)

        # Define SNMP command to use
        if self.__snmpcmd == 'get':
            snmpcmd = cmdgen.CommandGenerator().getCmd
        elif self.__snmpcmd == 'getnext':
            snmpcmd = cmdgen.CommandGenerator().nextCmd
        else:
            raise NagiosUnknown("Invalid SNMP command \'%s\' !" % self.__snmpcmd)

        # Convert dotted OID notation to a tuple if it is a dotted notation string
        if type(oid) is str:
            oid = self.__convert_oid_to_tuple(oid)

        try:
            errorIndication, errorStatus, errorIndex, varBinds = snmpcmd(
                cmdgen.CommunityData('nagios-plugin', self.__probe._community, self.__probe._snmpv2),
                self.__probe._udp_transport,
                oid
            )
            if errorIndication is not None:
                raise NagiosUnknown('SNMP query error: %s' % errorIndication)
        except Exception as e:
            raise NagiosUnknown(
                '''Unexpected error during SNMP %s query !\nHost: %s\nCommunity: %s\nOID: %s\nMessage: %s''' % (
                    self.__snmpcmd.upper(), self.__probe._hostaddress, self.__probe._community, oid, e))

        logger.debug('Returned varBinds:')
        logger.debug(pformat(varBinds, indent=8))

        return varBinds

    def execute(self):
        """
        Execute a SNMP query on OIDs and return the resulted (formatted) varBinds.
        """

        logger.debug('')
        logger.debug('=== BEGIN SNMP %s QUERY ===' % self.__snmpcmd.upper())

        # Prepare OIDs to fetch
        oids = self.__oids.values()
        varBindsTable = []
        results = {}

        # Fetch OID values
        for oid in oids:
            varBindsTable.extend(self.__get_raw_oid_values(oid))

        # Map varBinds to the user provided name for OIDs
        for datas in varBindsTable:
            if type(datas) is list:
                for varBind in datas:
                    oid, value = varBind
                    index = oid[-1]
                    oid_name = find_key_from_value(self.__oids, oid.prettyPrint())

                    if not results.has_key(oid_name):
                        results[oid_name] = []

                    results[oid_name].append((index, value))
            else:
                oid, value = datas
                print datas
                index = oid[-1]
                oid_name = find_key_from_value(self.__oids, oid.prettyPrint())

                results[oid_name] = (index, value)

        logger.debug('Returned results:')
        logger.debug(pformat(results, indent=4))
        logger.debug('=== END SNMP QUERY ===')

        return results

    def __convert_oid_to_tuple(self, oid_str):
        """Convert an OID string representation to a tuple (1,3,6,...)."""
        return tuple([int(chr) for chr in oid_str.split('.')])

    def __convert_tuple_to_oid(self, oid_tuple):
        """Convert an OID tuple representation to a string \"1.3.6...\"."""
        oid_str = [str(i) for i in oid_tuple]
        return ".".join(oid_str)


class ProbeSNMP(Probe):
    """
    Class ProbeSNMP.
    """

    def __init__(self, hostaddress='', port=161, community='public', snmpv2=False):
        super(ProbeSNMP, self).__init__(hostaddress, port)

        self._community = community
        self._snmpv2 = snmpv2

        try:
            logger.debug('Establishing SNMP connection to \'%s:%d\' with community \'%s\' using SNMPv2 (%s)...' % (
                self._hostaddress,
                self._port,
                self._community,
                self._snmpv2)
            )
            self._udp_transport = cmdgen.UdpTransportTarget((self._hostaddress, self._port))
        except Exception as e:
            raise NagiosUnknown(
                '''Cannot establish a SNMP connection !\nHost: %s\nCommunity: %s\nMessage: %s'''
                % (self._hostaddress, self._community, e))

        if 'ProbeSNMP' == self.__class__.__name__: logger.debug('=== END PROBE INIT ===')

    def get(self, oidstable):
        """
        Query a SNMP OID using Get command.
        """
        query = SNMPQuery(self, oidstable)
        return query.execute()

    def getnext(self, oidstable):
        """
        Query a SNMP OID using Getnext command.
        """
        query = SNMPQuery(self, oidstable, snmpcmd='getnext')
        return query.execute()
