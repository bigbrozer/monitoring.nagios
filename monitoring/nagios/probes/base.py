# -*- coding: utf-8 -*-
#===============================================================================
# Filename      : base
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : Base classes for probes.
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

logger = log.getLogger('monitoring.nagios.probes')

class Probe(object):
    """
    Base class for defining a new Probe.
    """

    def __init__(self, hostaddress='', port=None):
        logger.debug('')
        logger.debug('=== BEGIN NEW PROBE INIT ===')
        logger.debug('Instanciating a new probe of type %s.' % self.__class__.__name__)

        self._hostaddress = hostaddress
        self._port = port

        if 'Probe' == self.__class__.__name__: logger.debug('=== END PROBE INIT ===')