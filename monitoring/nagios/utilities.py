# -*- coding: UTF-8 -*-
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

"""Various utilities functions."""

from __future__ import division
from datetime import timedelta
import logging as log

logger = log.getLogger('monitoring.nagios.utilities')

__all__ = [
    'ip_rm_leading_zero',
    'humanize_bytes',
    'percent_used',
    'find_key_from_value',
    'humanize_duration',
]


def ip_rm_leading_zero(ip):
    """
    Remove leading zeros in IP address.

    String like '010.025.036.002' will return '10.25.36.2'.

    .. note::
       TODO: Write a nice example ;-)

    :param ip: IP address.
    :type ip: string
    :return: IP address with leading zeros removed as string.
    """
    return '.'.join([str(int(ip_elem)) for ip_elem in ip.split('.')])


def humanize_bytes(byte, precision=2):
    """
    Return a humanized string representation of a number of bytes.

    **Example**::

     >>> humanize_bytes(1024)
     '1.00 kB'

    :param byte: Byte number.
    :type byte: Integer.
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
        if byte >= factor:
            break
    return '%.*f %s' % (precision, byte / factor, suffix)


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
    pused = round((100. / total) * used, decimal)
    return pused


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
    :param sep: specify a separator for days, hours, minutes and seconds in the
                final string.
    :return: a dict with keys: ``days``, ``hours``, ``minutes``, ``minutes``
             and ``seconds``.
    :rtype: dict

    **Example**::

     >>> age = humanize_duration(timedelta(days=1, hours=2, minutes=34, seconds=22), sep=", ")
     >>> age
     {'timedelta': datetime.timedelta(1, 9262), 'seconds': 22, 'as_string': '1 days, 2 hours, 34 minutes, 22 seconds', 'days': 1, 'hours': 2, 'minutes': 34}
     >>> age_filter = humanize_duration(timedelta(days=1, hours=2, minutes=34, seconds=22), sep=", ", show=['days', 'hours'])
     >>> age_filter['as_string']
     '1 days, 2 hours'
    """
    if not show:
        show = ['days', 'hours', 'minutes', 'seconds']
    duration = {}
    as_string = []

    # Get data about duration
    duration['timedelta'] = time_delta
    duration['days'], remains = divmod(
        int(duration['timedelta'].total_seconds()),
        int(timedelta(days=1).total_seconds()))
    duration['hours'], remains = divmod(
        remains, int(timedelta(hours=1).total_seconds()))
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
