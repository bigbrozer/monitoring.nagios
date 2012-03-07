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

""":mod:`nagppt.utility` -- Some misc utility functions."""

from __future__ import division

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