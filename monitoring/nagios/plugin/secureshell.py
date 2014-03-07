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

"""SSH module for plugins."""

import logging as log

from monitoring.nagios.plugin import NagiosPlugin
from monitoring.nagios.probes import ProbeSSH

logger = log.getLogger('monitoring.nagios.plugin.ssh')


class NagiosPluginSSH(NagiosPlugin):
    """Base for a standard SSH Nagios plugin"""
    def __init__(self, *args, **kwargs):
        super(NagiosPluginSSH, self).__init__(*args, **kwargs)

        # Init a new probe of type SSH
        self.ssh = ProbeSSH(
            hostaddress=self.options.hostname,
            port=self.options.port,
            username=self.options.username,
            password=self.options.password,
            timeout=self.options.timeout
        )

        if 'NagiosPluginSSH' == self.__class__.__name__:
            logger.debug('=== END PLUGIN INIT ===')

    def define_plugin_arguments(self):
        """Define arguments for the plugin"""
        super(NagiosPluginSSH, self).define_plugin_arguments()

        # Add extra arguments
        self.parser.add_argument('-u', '--username',
                                 dest='username',
                                 default=None,
                                 help='Login user. Default to current logged '
                                      'in user.',
                                 required=False)
        self.parser.add_argument('-p', '--password',
                                 dest='password',
                                 default=None,
                                 help='Login user password. Default is to use '
                                      'pub key of the current user.',
                                 required=False)
        self.parser.add_argument('-P',
                                 type=int,
                                 dest='port',
                                 default=22,
                                 help='Port to connect to (default to 22).')
        self.parser.add_argument('-t', '--timeout',
                                 type=float,
                                 dest='timeout',
                                 default=10,
                                 help='Connection timeout in seconds (default '
                                      'to 10 secs).')

    def verify_plugin_arguments(self):
        """Check syntax of all arguments"""
        super(NagiosPluginSSH, self).verify_plugin_arguments()
