# -*- coding: utf-8 -*-
# Copyright (C) Vincent BESANCON <besancon.vincent@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""SNMP probe module."""

import logging as log
from pprint import pformat
from pysnmp.entity.rfc3413.oneliner import cmdgen
from UserDict import IterableUserDict

from monitoring.nagios.probes import Probe
from monitoring.nagios.plugin.exceptions import NagiosUnknown
from monitoring.nagios.plugin.utilities import find_key_from_value

logger = log.getLogger('monitoring.nagios.probes')


class _OidValue(object):
    """Class that represents a value from an OID."""
    def __init__(self, varBind):
        oid, value = varBind

        self.index = oid[-1]
        self.oid = oid.prettyPrint()
        self.value = value

        logger.debug('-- Instance of OidValue created: %r', self)

    def pretty(self):
        """Return the pretty format of a value."""
        return self.value.prettyPrint()

    def __str__(self):
        return self.value.prettyPrint()

    def __repr__(self):
        return '{0}({1}, {2})'.format(
            self.__class__.__name__,
            repr(self.oid),
            repr(self.value),
        )


class _SNMPQuery(object):
    """
    Class that construct a SNMP query.

    This is used internally. Should not be used separatly.
    """
    def __init__(self, probe, oidstable, snmpcmd='get'):
        self.__probe = probe
        self.__oids = oidstable
        self.__snmpcmd = snmpcmd

    def __get_raw_oid_values(self, oidinfo):
        """
        Launch a SNMP query on a OID (name, oid).

        Return raw data as a list.
        """
        name, oid = oidinfo

        logger.debug('-- Probing OID \'%s\': %s ...', name, oid)

        # Define SNMP command to use
        if self.__snmpcmd == 'get':
            snmpcmd = cmdgen.CommandGenerator().getCmd
        elif self.__snmpcmd == 'getnext':
            snmpcmd = cmdgen.CommandGenerator().nextCmd
        else:
            raise NagiosUnknown(
                "Invalid SNMP command \'%s\' !" % self.__snmpcmd)

        # Convert dotted OID notation to a tuple if it is a dotted notation
        # string
        if type(oid) is str:
            oid = self.__convert_oid_to_tuple(oid)

        try:
            errorIndication, _, _, varBinds = snmpcmd(
                cmdgen.CommunityData('nagios-plugin', self.__probe._community,
                                     self.__probe._snmpv2),
                self.__probe._udp_transport, oid)
            if errorIndication is not None:
                raise NagiosUnknown('SNMP query error: %s' % errorIndication)
        except Exception as e:
            raise NagiosUnknown('Unexpected error during SNMP %s query !\n'
                                'Host: %s\n'
                                'Community: %s\n'
                                'OID: %s\n'
                                'Message: %s' % (self.__snmpcmd.upper(),
                                                 self.__probe._hostaddress,
                                                 self.__probe._community, oid,
                                                 e))

        logger.debug('Returned varBinds:')
        logger.debug(pformat(varBinds, indent=4))

        return varBinds

    def execute(self):
        """Execute a SNMP query on OIDs and return the resulted (formatted)
        varBinds."""
        logger.debug('')
        logger.debug('=== BEGIN SNMP %s QUERY ===', self.__snmpcmd.upper())

        # Prepare OIDs to fetch
        varBindsTable = []
        results = {}

        # Fetch OID values
        for oid in self.__oids.iteritems():
            varBindsTable.extend(self.__get_raw_oid_values(oid))

        # Map varBinds to the user provided name for OIDs
        for varBinds in varBindsTable:
            if type(varBinds) is list:
                for varBind in varBinds:
                    data = _OidValue(varBind)
                    oid_name = find_key_from_value(self.__oids, data.oid)

                    if not oid_name in results:
                        results[oid_name] = []

                    results[oid_name].append(data)
            else:
                data = _OidValue(varBinds)
                oid_name = find_key_from_value(self.__oids, data.oid)

                results[oid_name] = data

        logger.debug('=== END SNMP QUERY ===')

        return results

    def __convert_oid_to_tuple(self, oid_str):
        """Convert an OID string representation to a tuple (1,3,6,...)."""
        return tuple([int(c) for c in oid_str.split('.')])

    def __convert_tuple_to_oid(self, oid_tuple):
        """Convert an OID tuple representation to a string \"1.3.6...\"."""
        oid_str = [str(i) for i in oid_tuple]
        return ".".join(oid_str)


class _SNMPTable(IterableUserDict):
    """Construct a SNMP table. This is not a full table like in MIBs."""
    def __init__(self, probe, columns):
        logger.debug('=== BEGIN NEW SNMP TABLE===')

        # This is the SNMP probe that handle SNMP communication
        self.__probe = probe

        # Get indexes and oid values
        indexes = self.__probe.getnext(
            {'indexes': columns.pop('indexes')})['indexes']

        # Append index to all OIDs
        values = dict.fromkeys(columns, list())
        for _, index in indexes:
            cols = {}
            for name, oid in columns.viewitems():
                o = '%s.%s' % (oid, index)
                cols[name] = o
            # Query values
            results = self.__probe.get(cols)
            for k, v in results.viewitems():
                values[k].append(v)
                print values

        IterableUserDict.__init__(self, values)

        logger.debug('=== BEGIN NEW SNMP TABLE===')


class ProbeSNMP(Probe):
    """Class ProbeSNMP."""
    def __init__(self, hostaddress='', port=161, community='public',
                 snmpv2=False):
        super(ProbeSNMP, self).__init__(hostaddress, port)

        self._community = community
        self._snmpv2 = snmpv2

        try:
            logger.debug('Establishing SNMP connection to \'%s:%d\' with '
                         'community \'%s\' using SNMPv2 (%s)...',
                         self._hostaddress, self._port, self._community,
                         self._snmpv2)
            self._udp_transport = cmdgen.UdpTransportTarget(
                (self._hostaddress, self._port))
        except Exception as e:
            raise NagiosUnknown('Cannot establish a SNMP connection !\n'
                                'Host: %s\n'
                                'Community: %s\n'
                                'Message: %s' % (self._hostaddress,
                                                 self._community, e))

        if 'ProbeSNMP' == self.__class__.__name__:
            logger.debug('=== END PROBE INIT ===')

    def get(self, oidstable):
        """Query a SNMP OID using Get command."""
        query = _SNMPQuery(self, oidstable)
        return query.execute()

    def getnext(self, oidstable):
        """Query a SNMP OID using Getnext command."""
        query = _SNMPQuery(self, oidstable, snmpcmd='getnext')
        return query.execute()

    def table(self, columns):
        """
        Query SNMP OIDs and format results like a table.

        NOT YET IMPLEMENTED.
        """
        raise NotImplementedError('Method table() of ProbeSNMP instances '
                                  'will be implemented in next release !')
