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

"""WMI module for plugins."""

import logging
import csv
from pprint import pformat

from monitoring.nagios.plugin import NagiosPlugin
from monitoring.nagios.probes import ProbeWMI

logger = logging.getLogger('monitoring.nagios.plugin.wmi')


class NagiosPluginWMI(NagiosPlugin):
    """Base for a standard WMI Nagios plugin"""
    def __init__(self, *args, **kwargs):
        super(NagiosPluginWMI, self).__init__(*args, **kwargs)

        # Init a new probe of type WMI
        self.probe = ProbeWMI(
            hostaddress=self.options.hostname,
            login=self.options.login,
            password=self.options.password,
            domain=self.options.domain,
            namespace=self.options.namespace
        )

        if 'NagiosPluginWMI' == self.__class__.__name__:
            logger.debug('=== END PLUGIN INIT ===')

    def define_plugin_arguments(self):
        """Define arguments for the plugin"""
        super(NagiosPluginWMI, self).define_plugin_arguments()

        # Add extra arguments
        self.parser.add_argument('-l', '--login',
                                 dest='login',
                                 help='Login for the WMI remote call.',
                                 required=True)
        self.parser.add_argument('-p', '--password',
                                 dest='password',
                                 help='Login password for the WMI remote '
                                      'call.',
                                 required=True)

        self.parser.add_argument('-d', '--domain',
                                 dest='domain',
                                 help='Login AD domain for the WMI remote '
                                      'call.',
                                 required=True)

        self.parser.add_argument('-n', '--namespace',
                                 dest='namespace',
                                 default='root/cimv2',
                                 help='WMI namespace (default to root/cimv2).')

    def verify_plugin_arguments(self):
        """Check syntax of all arguments"""
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
            self.unknown('Error during the WMI query !\n'
                         'Command: {0.cmd}\nOutput: {0.output}'.format(e))

        # Split lines in list, remove headers
        wmic_output = wmic_output.splitlines()[1:]

        # Parse CSV result
        csv_reader = csv.DictReader(wmic_output, delimiter='|')
        query_results = list(csv_reader)

        logger.debug('WMI results:\n%s', pformat(query_results))

        return query_results
