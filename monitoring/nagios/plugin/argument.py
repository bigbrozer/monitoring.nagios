# -*- coding: utf-8 -*-
#===============================================================================
# Filename      : arguments
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : Specify, apply type conversion, etc... for arguments.
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

:mod:`monitoring.nagios.plugin.arguments` --- Argument conversion and specification
===================================================================================

This module contains a set of functions to convert or specify argument types.
"""

from datetime import timedelta

def hours(hour):
    """
    Set argument type to hour. Convert ``hour`` to a timedelta object.

    :param hour: the number of hour.
    :type hour: str, unicode
    :return: Equivalent to ``timedelta(hours=hour)``
    :rtype: timedelta
    """
    return timedelta(hours=int(hour))
