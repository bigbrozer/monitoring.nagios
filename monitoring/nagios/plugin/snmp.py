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

"""SNMP module for plugins."""

import logging as log

from monitoring.nagios.probes import ProbeSNMP
from monitoring.nagios.plugin import NagiosPlugin

logger = log.getLogger('monitoring.nagios.plugin.snmp')


class NagiosPluginSNMP(NagiosPlugin):
    """A standard SNMP Nagios plugin."""
    def __init__(self, *args, **kwargs):
        super(NagiosPluginSNMP, self).__init__(*args, **kwargs)

        self.__use_snmp_v2 = 0

        # Init a new probe of type SNMP
        self.snmp = ProbeSNMP(
            hostaddress=self.options.hostname,
            community=self.options.snmpcommunity,
            snmpv2=self.options.snmpv2
        )

        if 'NagiosPluginSNMP' == self.__class__.__name__:
            logger.debug('=== END PLUGIN INIT ===')

    def define_plugin_arguments(self):
        """Define arguments for the plugin"""
        super(NagiosPluginSNMP, self).define_plugin_arguments()

        # Add extra arguments
        self.required_args.add_argument('-C',
                                        dest='snmpcommunity',
                                        help='SNMP Community to use',
                                        required=True)
        self.parser.add_argument('-2',
                                 action='store_true',
                                 dest='snmpv2',
                                 default=False,
                                 help='Use SNMP v2c (default use version 1)')
        self.parser.add_argument('-p',
                                 type=int,
                                 dest='port',
                                 default=161,
                                 help='Port to connect to (default to 161).')

    def verify_plugin_arguments(self):
        """Check syntax of all arguments"""
        super(NagiosPluginSNMP, self).verify_plugin_arguments()

        if self.options.snmpv2:
            logger.debug('Using SNMP v2.')
            self.__use_snmp_v2 = 1
