# -*- coding: utf-8 -*-
#===============================================================================
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : This is a list of pre-defined argument types.
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

"""
.. module:: monitoring.nagios.plugin.arguments

:mod:`monitoring.nagios.plugin.arguments` --- Pre-defined argument types
========================================================================

This module contains a set of functions to convert or specify argument types.
"""

from datetime import timedelta


def days(integer):
    """
    Convert ``integer`` to a timedelta object. ``integer`` is a number of days.

    :param integer: the number of days.
    :type integer: str, unicode
    :return: the number of days as a timedelta object.
    :rtype: timedelta

    # Tests
    >>> days(5)
    datetime.timedelta(5)
    """
    return timedelta(days=int(integer))

def hours(integer):
    """
    Convert ``integer`` to a timedelta object. ``integer`` is a number of hours.

    :param integer: the number of hours.
    :type integer: str, unicode
    :return: the number of hours as a timedelta object.
    :rtype: timedelta

    # Tests
    >>> hours(4)
    datetime.timedelta(0, 14400)
    """
    return timedelta(hours=int(integer))

def minutes(integer):
    """
    Convert ``integer`` to a timedelta object. ``integer`` is a number of
    minutes.

    :param integer: the number of minutes.
    :type integer: str, unicode
    :return: the number of minutes as a timedelta object.
    :rtype: timedelta

    # Tests
    >>> minutes(32)
    datetime.timedelta(0, 1920)
    """
    return timedelta(minutes=int(integer))

def seconds(integer):
    """
    Convert ``integer`` to a timedelta object. ``integer`` is a number of
    seconds.

    :param integer: the number of seconds.
    :type integer: str, unicode
    :return: the number of seconds as a timedelta object.
    :rtype: timedelta

    # Tests
    >>> seconds(54)
    datetime.timedelta(0, 54)
    """
    return timedelta(seconds=int(integer))
