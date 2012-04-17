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
from monitoring.nagios.plugin.utilities import find_key_from_value

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
    class __SNMPQuery(object):
        """
        Class that construct a SNMP query.
        """
        def __init__(self, probe, oids, snmpcmd='get'):
            self.__probe = probe
            self.__oids = oids
            self.__snmpcmd = snmpcmd

        def execute(self):
            """
            Execute a SNMP query on OIDs and return the resulted varBinds.
            """
            logger.debug('')
            logger.debug('=== BEGIN SNMP %s QUERY ===' % self.__snmpcmd.upper())

            # Store query results to returns
            results = {}

            # Define SNMP command to use
            if self.__snmpcmd == 'get':
                snmpcmd = cmdgen.CommandGenerator().getCmd
            elif self.__snmpcmd == 'getnext':
                snmpcmd = cmdgen.CommandGenerator().nextCmd
            else:
                raise NagiosUnknown("Invalid SNMP command \'%s\' !" % self.__snmpcmd)

            # Prepare OIDs to fetch
            oids = self.__oids.values()

            # Convert dotted OID notation to a tuple if it is a dotted notation string
            for o in oids:
                i = oids.index(o)
                if type(o) is str:
                    oids[i] = self.__convert_oid_to_tuple(o)

            try:
                logger.debug('Establishing SNMP connection to \'%s:%d\' with community \'%s\' using SNMPv2 (%s)...' % (
                    self.__probe._hostaddress,
                    self.__probe._port,
                    self.__probe._community,
                    self.__probe._snmpv2)
                )
                errorIndication, errorStatus, errorIndex, varBinds = snmpcmd(
                    cmdgen.CommunityData('nagios-plugin', self.__probe._community, self.__probe._snmpv2),
                    cmdgen.UdpTransportTarget((self.__probe._hostaddress, self.__probe._port)),
                    *oids
                )
            except Exception as e:
                raise NagiosUnknown('''Unexpected error during SNMP %s query !\nHost: %s\nCommunity: %s\nOID: %s\nMessage: %s''' % (
                    self.__snmpcmd.upper(), self.__probe._hostaddress, self.__probe._community, oids, e))

            if errorIndication is not None: raise NagiosUnknown('SNMP query error: %s' % errorIndication)

            logger.debug('Returned Varbinds:')
            logger.debug(pformat(varBinds, indent=4))

            # Map varBinds to the user provided name for OIDs
            for datas in varBinds:
                if type(datas) is list:
                    for varBind in datas:
                        oid, value = varBind
                        oid = oid.prettyPrint()
                        oid_name = find_key_from_value(self.__oids, oid)

                        if not results.has_key(oid_name):
                            results[oid_name] = []
                        else:
                            results[oid_name].append(value)
                else:
                    oid, value = datas
                    oid = oid.prettyPrint()
                    oid_name = find_key_from_value(self.__oids, oid)

                    results[oid_name] = value

            logger.debug('Returned results:')
            logger.debug(pformat(results, indent=4))
            logger.debug('=== END SNMP QUERY ===')

            return results

            # Private methods for internal processing
        def __convert_oid_to_tuple(self, oid_str):
            logger.debug('-- Converting OID string to Tuple: %s' % oid_str)
            return tuple([int(chr) for chr in oid_str.split('.')])

        def __convert_tuple_to_oid(self, oid_tuple):
            logger.debug('-- Converting OID Tuple to string: %s' % oid_tuple)
            oid_str = [str(i) for i in oid_tuple]
            return ".".join(oid_str)

    def __init__(self, hostaddress='', port=161, community='public', snmpv2=False):
        super(ProbeSNMP, self).__init__(hostaddress, port)

        self._community = community
        self._snmpv2 = snmpv2

        logger.debug('Probe attributes:')
        logger.debug(pformat(vars(self), indent=4))

        if 'ProbeSNMP' == self.__class__.__name__: logger.debug('=== END PROBE INIT ===')

    # Public methods
    # ==============
    #
    def get(self, **oids):
        """
        Query a SNMP OID using Get command.
        """
        query = self.__query(oids)
        return query.execute()

    def getnext(self, **oids):
        """
        Query a SNMP OID using Getnext command.
        """
        query = self.__query(oids, snmpcmd='getnext')
        return query.execute()

    # Private methods
    # ==============
    #
    def __query(self, settings, snmpcmd='get'):
        return self.__SNMPQuery(self, settings, snmpcmd)