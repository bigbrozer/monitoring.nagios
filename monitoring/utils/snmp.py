# -*- coding: UTF-8 -*-
#===============================================================================
# Filename      : snmp
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : Utility functions to use SNMP protocol (Get, Next, Convert...)
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

from pysnmp.entity.rfc3413.oneliner import cmdgen
from monitoring.nagios.plugin.exceptions import NagiosUnknown

logger = log.getLogger('monitoring.utils.snmp')

def snmp_next(host, community, oid_param, port=161, snmpv2=True):
    """
            Query a SNMP OID and return all results as a list

            Return a list:
                [[(OID), Value]...]
    """
    logger.debug('Query SNMP Next on host %s for OID %s.' % (host, oid_param))

    values = []
    oid = None

    # Convert dotted OID notation to a tuple
    if type(oid_param) is str:
        oid = convert_oid_to_tuple(oid_param)
    try:
        errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().nextCmd(
            cmdgen.CommunityData('nagios-plugin', community, snmpv2),
            cmdgen.UdpTransportTarget((host, port)),
            oid
        )
    except Exception as e:
        raise NagiosUnknown('''Unexpected error during SNMP Getnext query !\nHost: %s\nCommunity: %s\nOID: %s\nMessage: %s''' % (
            host, community, oid_param, e))

    if errorIndication is not None: raise NagiosUnknown('SNMP query error: %s' % errorIndication)

    for varBind in varBinds:
        values.append(varBind[0])

    logger.debug('\tVarbinds: %s' % values)

    return values

def snmp_get(host, community, oid_param, port=161, snmpv2=True):
    """
            Query a SNMP OID and return the result

            Return a single element list:
                [(OID), Value]
    """
    logger.debug('Query SNMP Get on host %s for OID %s.' % (host, oid_param))

    oid = None

    # Convert dotted OID notation to a tuple if it is a dotted notation string
    if type(oid_param) is str:
        oid = convert_oid_to_tuple(oid_param)

    try:
        errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(
            cmdgen.CommunityData('nagios-plugin', community, snmpv2),
            cmdgen.UdpTransportTarget((host, port)),
            oid
        )
    except Exception as e:
        raise NagiosUnknown('''Unexpected error during SNMP Get query !\nHost: %s\nCommunity: %s\nOID: %s\nMessage: %s''' % (
            host, community, oid_param, e))

    if errorIndication is not None: raise NagiosUnknown('SNMP query error: %s' % errorIndication)

    logger.debug('\tVarbinds: %s' % varBinds)

    return varBinds[0]

def convert_oid_to_tuple(oid_str):
    logger.debug('Converting OID string to Tuple: %s' % oid_str)
    return tuple([int(chr) for chr in oid_str.split('.')])

def convert_tuple_to_oid(oid_tuple):
    logger.debug('Converting OID Tuple to string: %s' % oid_tuple)
    oid_str = [str(i) for i in oid_tuple]
    return ".".join(oid_str)