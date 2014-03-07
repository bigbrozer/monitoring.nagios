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

"""WMI probe module."""

import logging
import subprocess as sp

from monitoring.nagios.probes import Probe

logger = logging.getLogger('monitoring.nagios.probes')


class ProbeWMI(Probe):
    """
    A WMI probe.

    :param hostaddress: The IP address of host to connect to.
    :type hostaddress: str
    :param login: Login name.
    :type login: str
    :param password: Login password.
    :type password: str
    :param domain: Login AD domain.
    :type domain: str
    :param namespace: WMI namespace (default is ``root/cimv2``).
    :type namespace: str
    """
    def __init__(self,
                 hostaddress,
                 login,
                 password,
                 domain,
                 namespace='root/cimv2'):
        super(ProbeWMI, self).__init__()

        self.hostaddress = hostaddress
        self.login = login
        self._password = password
        self.domain = domain
        self.credentials = "{0.domain}\\{0.login}%{0._password}".format(self)
        self.hosturl = "//{0.hostaddress}".format(self)
        self.namespace = namespace
        self.command = []

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
