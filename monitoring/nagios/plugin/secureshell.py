# -*- coding: utf-8 -*-
#===============================================================================
# Filename      : monitoring.nagios.plugin.secureshell
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : Class to define a standard Nagios SSH plugin.
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
import os
import sys

from monitoring.nagios.plugin import NagiosPlugin
from monitoring.nagios.probes import ProbeSSH

logger = log.getLogger('monitoring.nagios.plugin.ssh')


class NagiosPluginSSH(NagiosPlugin):
    """Base for a standard SSH Nagios plugin"""

    def __init__(self, name=os.path.basename(sys.argv[0]), version='', description=''):
        super(NagiosPluginSSH, self).__init__(name, version, description)

        # Init a new probe of type SSH
        self.ssh = ProbeSSH(
            hostaddress=self.options.hostname,
            port=self.options.port,
            username=self.options.username,
            password=self.options.password,
        )

        if 'NagiosPluginSSH' == self.__class__.__name__: logger.debug('=== END PLUGIN INIT ===')

    def define_plugin_arguments(self):
        """Define arguments for the plugin"""
        # Define common arguments
        super(NagiosPluginSSH, self).define_plugin_arguments()

        # Add extra arguments
        self.parser.add_argument('-u', '--username', dest='username', default=None,
                                 help='Login user. Default to current logged in user.', required=False)
        self.parser.add_argument('-p', '--password', dest='password', default=None,
                                 help='Login user password. Default is to use pub key of the current user.',
                                 required=False)
        self.parser.add_argument('-P', type=int, dest='port', default=22, help='Port to connect to (default to 22).')
        self.parser.add_argument('-t', '--timeout', type=float, dest='timeout', default=10, help='Connection timeout in seconds (default to 10 secs).')

    def verify_plugin_arguments(self):
        """Check syntax of all arguments"""
        # Check common arguments syntax
        super(NagiosPluginSSH, self).verify_plugin_arguments()
