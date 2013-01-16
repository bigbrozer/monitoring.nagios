# -*- coding: UTF-8 -*-
#===============================================================================
# Filename      : utilities
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : Various utility functions.
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

from __future__ import division
from datetime import timedelta
import logging as log

logger = log.getLogger('monitoring.nagios.plugin.utilities')

__all__ = [
    'ip_rm_leading_zero',
    'humanize_bytes',
    'percent_used',
    'find_key_from_value',
    'humanize_duration',
]

def ip_rm_leading_zero(ip):
    """
    Remove leading zeros in IP address string like '010.025.036.002'. Return '10.25.36.2'.

    .. note::
       TODO: Write a nice example ;-)

    :param ip: IP address.
    :type ip: string
    :return: IP address with leading zeros removed as string.
    """
    return '.'.join([str(int(ip_elem)) for ip_elem in ip.split('.')])

def humanize_bytes(bytes, precision=2):
    """
    Return a humanized string representation of a number of bytes.

    **Example**::

      print humanize_bytes(1024)

      --> It will return: "1 kB"

    :param bytes: Byte number.
    :type bytes: Integer.
    :param precision: Specify float precision after conversion (default 2).
    :type precision: Integer.
    :return: Humanized string representation of a number of bytes.
    """
    units = (
        (1 << 50L, 'PB'),
        (1 << 40L, 'TB'),
        (1 << 30L, 'GB'),
        (1 << 20L, 'MB'),
        (1 << 10L, 'kB'),
        (1, 'byte(s)')
        )

    for factor, suffix in units:
        if bytes >= factor:
            break
    return '%.*f %s' % (precision, bytes / factor, suffix)

def percent_used(used, total, decimal=2):
    """
    Return percent used by giving total and used value.

    :param used: Used value.
    :type used: Integer
    :param total: Total value.
    :type total: Integer
    :return: Float for percent used.
    :rtype: Float
    """
    percent_used = round((100. / total) * used, decimal)
    return percent_used

def find_key_from_value(dic, val):
    """
    Return the key of dictionary dic given the value

    :param dic: dict to search in.
    :type dic: dict
    :param val: the value you need the key.
    """
    return [k for k, v in dic.iteritems() if v in val][0]

def humanize_duration(time_delta, show=None, sep=" "):
    """
    Humanize a timedelta object.

    :param time_delta: the timedelta object to humanize.
    :param sep: specify a separator for days, hours, minutes and seconds in the final string.
    :return: a dict with keys: ``days``, ``hours``, ``minutes``, ``minutes`` and ``seconds``.
    :rtype: dict

    **Example**::

     >>> age = humanize_duration(timedelta(days=1, hours=2, minutes=34, seconds=22), sep=", ")
     >>> age
     {'timedelta': datetime.timedelta(1, 9262), 'seconds': 22, 'as_string': '1 days, 2 hours, 34 minutes, 22 seconds', 'days': 1, 'hours': 2, 'minutes': 34}
     >>> age_filter = humanize_duration(timedelta(days=1, hours=2, minutes=34, seconds=22), sep=", ", show=['days', 'hours'])
     >>> age_filter['as_string']
     '1 days, 2 hours'
    """
    if not show: show = ['days', 'hours', 'minutes', 'seconds']
    duration = {}
    as_string = []

    # Get data about duration
    duration['timedelta'] = time_delta
    duration['days'], remains = divmod(int(duration['timedelta'].total_seconds()), int(timedelta(days=1).total_seconds()))
    duration['hours'], remains = divmod(remains, int(timedelta(hours=1).total_seconds()))
    duration['minutes'], remains = divmod(remains, 60)
    duration['seconds'] = int(remains)

    if duration['days'] and 'days' in show:
        as_string.append('{days} days')
    if duration['hours'] and 'hours' in show:
        as_string.append('{hours} hours')
    if duration['minutes'] and 'minutes' in show:
        as_string.append('{minutes} minutes')
    if 'seconds' in show or not as_string:
        as_string.append('{seconds} seconds')
    as_string = sep.join(as_string).format(**duration)

    duration['as_string'] = as_string

    return duration
