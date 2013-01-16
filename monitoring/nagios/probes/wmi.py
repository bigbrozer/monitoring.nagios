# -*- coding: utf-8 -*-
#===============================================================================
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : Module that define a WMI probe (make use of wmic).
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

import logging
import subprocess as sp

from monitoring.nagios.probes import Probe

logger = logging.getLogger('monitoring.nagios.probes')


class ProbeWMI(Probe):
    """
    A WMI probe.

    :param host: The IP address of host to connect to.
    :type host: str
    :param login: Login name.
    :type login: str
    :param password: Login password.
    :type password: str
    :param domain: Login AD domain.
    :type domain: str
    :param namespace: WMI namespace (default is ``root/cimv2``).
    :type namespace: str
    """
    
    def __init__(self, host, login, password, domain, namespace='root/cimv2'):
        super(ProbeWMI, self).__init__(host)

        self.credentials = '{0}\{1}%{2}'.format(domain, login, password)
        self.hosturl = '//{0}'.format(host)
        self.namespace = namespace

    def execute(self, query):
        """
        Execute a WMI query on the remote server and return results.

        :param query: The WMI query.
        :type query: str, unicode
        :return: CSV with delimiter ``|``.
        """
        self.command = [
            'wmic',
            '-U', self.credentials,
            self.hosturl,
            '--namespace', self.namespace,
            query,
        ]

        logger.debug('Executing command: %s', " ".join(self.command))
        wmic_output = sp.check_output(self.command)

        return wmic_output
