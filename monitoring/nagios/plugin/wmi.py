# -*- coding: utf-8 -*-
#===============================================================================
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : Class to define a standard Nagios WMI plugin.
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
import os
import sys
import csv
from pprint import pformat

from monitoring.nagios.plugin import NagiosPlugin
from monitoring.nagios.probes import ProbeWMI

logger = logging.getLogger('monitoring.nagios.plugin.wmi')


class NagiosPluginWMI(NagiosPlugin):
    """Base for a standard WMI Nagios plugin"""

    def __init__(self, name=os.path.basename(sys.argv[0]), version='', description=''):
        super(NagiosPluginWMI, self).__init__(name, version, description)

        # Init a new probe of type WMI
        self.probe = ProbeWMI(
            host=self.options.hostname,
            login=self.options.login,
            password=self.options.password,
            domain=self.options.domain,
            namespace=self.options.namespace
        )

        if 'NagiosPluginWMI' == self.__class__.__name__: logger.debug('=== END PLUGIN INIT ===')

    def define_plugin_arguments(self):
        """Define arguments for the plugin"""
        # Define common arguments
        super(NagiosPluginWMI, self).define_plugin_arguments()

        # Add extra arguments
        self.parser.add_argument('-l', '--login',
                                 dest='login',
                                 help='Login for the WMI remote call.',
                                 required=True)
        self.parser.add_argument('-p', '--password',
                                 dest='password',
                                 help='Login password for the WMI remote call.',
                                 required=True)
        
        self.parser.add_argument('-d', '--domain',
                                 dest='domain',
                                 help='Login AD domain for the WMI remote call.',
                                 required=True)

        self.parser.add_argument('-n', '--namespace',
                                 dest='namespace',
                                 default='root/cimv2',
                                 help='WMI namespace (default to root/cimv2).')

    def verify_plugin_arguments(self):
        """Check syntax of all arguments"""
        # Check common arguments syntax
        super(NagiosPluginWMI, self).verify_plugin_arguments()

    def execute(self, query):
        """
        Wrapper arround :meth:`monitoring.nagios.probes.ProbeWMI.execute`
        method. Handles exceptions and parse CSV results.

        :return: A dict with keys as WMI columns and their values.
        :rtype: dict
        """
        wmic_output = None

        try:
            wmic_output = self.probe.execute(query)
        except OSError:
            self.unknown('Unable to find \'wmic\' binary !')
        except Exception as e:
            self.unknown('Error during the WMI query !\nCommand: {0.cmd}\nOutput: {0.output}'.format(e))

        # Split lines in list, remove headers
        wmic_output = wmic_output.splitlines()[1:]

        # Parse CSV result
        csv_reader = csv.DictReader(wmic_output, delimiter='|')
        query_results = list(csv_reader)

        logger.debug('WMI results:\n%s', pformat(query_results))

        return query_results
