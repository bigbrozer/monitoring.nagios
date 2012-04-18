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

from pprint import pformat, pprint
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

        def __init__(self, probe, oidstable, snmpcmd='get', show_index=False):
            self.__probe = probe
            self.__oids = oidstable
            self.__snmpcmd = snmpcmd
            self.__with_index = show_index

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
                raise NagiosUnknown(
                    '''Unexpected error during SNMP %s query !\nHost: %s\nCommunity: %s\nOID: %s\nMessage: %s''' % (
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
                        index = oid.split('.')[-1]
                        value_with_index = {'index': index, 'val': value}
                        oid_name = find_key_from_value(self.__oids, oid)

                        if not results.has_key(oid_name):
                            results[oid_name] = []
                        else:
                            if self.__with_index:
                                results[oid_name].append(value_with_index)
                            else:
                                results[oid_name].append(value)
                else:
                    oid, value = datas
                    oid = oid.prettyPrint()
                    index = oid.split('.')[-1]
                    value_with_index = {'index': index, 'val': value}
                    oid_name = find_key_from_value(self.__oids, oid)

                    if self.__with_index:
                        results[oid_name] = value_with_index
                    else:
                        results[oid_name] = value

            logger.debug('Returned results:')
            logger.debug(pformat(results, indent=4))
            logger.debug('=== END SNMP QUERY ===')

            return results

        def __convert_oid_to_tuple(self, oid_str):
            logger.debug('-- Converting OID string to Tuple: %s' % oid_str)
            return tuple([int(chr) for chr in oid_str.split('.')])

        def __convert_tuple_to_oid(self, oid_tuple):
            logger.debug('-- Converting OID Tuple to string: %s' % oid_tuple)
            oid_str = [str(i) for i in oid_tuple]
            return ".".join(oid_str)

    class __SNMPTable(object):
        """
        Represent a SNMP Table.
        """

        def __init__(self, columns, primary_key=''):
            logger.debug('')
            logger.debug('=== BEGIN NEW SNMP TABLE ===')
            logger.debug('Initializing a new SNMP table...')
            self.__keys = columns.pop(primary_key)
            self.__cols = columns
            self.__table = {}

            logger.debug('Populating SNMP table...')
            for primary_keys in self.__keys:
                keyindex = primary_keys['index']
                key = primary_keys['val']
                key = key.prettyPrint()
                if key:
                    if not self.__table.has_key(key):
                        logger.debug('\tCreating key \'%s\' with key index \'%s\'.' % (key, keyindex))
                        self.__table[key] = {}

                    # Find data associated to the key
                    colvalues = {}
                    for colname, coldatas in self.__cols.viewitems():
                        for col in coldatas:
                            if keyindex == col['index']:
                                logger.debug('\t\tAdd key \'%s\' (keyindex: %s, colindex: %s) with value \'%s\'.' % (
                                colname, keyindex, col['index'], col['val']))
                                colvalues.update({colname: col['val']})
                            if self.__table[key].has_key(colname):
                                raise NagiosUnknown(
                                    'Error: redefine your primary key oid \'%s\', you may loose data because primary ' \
                                    'keys are not unique in this OID ! I have found multiple values for key \'%s\'.'
                                    % (primary_key, key))

                    self.__table[key].update(colvalues)

            logger.debug('=== END SNMP TABLE ===')

        def __getitem__(self, item):
            return self.__table.__getitem__(item)

        def __str__(self):
            return str(self.__table)

        def keys(self):
            return self.__table.keys()

    def __init__(self, hostaddress='', port=161, community='public', snmpv2=False):
        super(ProbeSNMP, self).__init__(hostaddress, port)

        self._community = community
        self._snmpv2 = snmpv2

        logger.debug('Probe attributes:')
        logger.debug(pformat(vars(self), indent=4))

        if 'ProbeSNMP' == self.__class__.__name__: logger.debug('=== END PROBE INIT ===')

    def get(self, oidstable, show_index=False):
        """
        Query a SNMP OID using Get command.
        """
        query = self.__SNMPQuery(self, oidstable, show_index=show_index)
        return query.execute()

    def getnext(self, oidstable, show_index=False):
        """
        Query a SNMP OID using Getnext command.
        """
        query = self.__SNMPQuery(self, oidstable, snmpcmd='getnext', show_index=show_index)
        return query.execute()

    def table(self, oidstable, primary_key=''):
        """
        Query a SNMP OID and return data as a table of values.
        """
        columns = self.__SNMPQuery(self, oidstable, snmpcmd='getnext', show_index=True).execute()
        table = self.__SNMPTable(columns, primary_key)
        return table
