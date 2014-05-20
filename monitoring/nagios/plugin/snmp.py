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

from monitoring.nagios.plugin import argument
from monitoring.nagios.probes import ProbeSNMP
from monitoring.nagios.plugin import NagiosPlugin

logger = log.getLogger('monitoring.nagios.plugin.snmp')


class NagiosPluginSNMP(NagiosPlugin):
    """A standard SNMP Nagios plugin."""
    def __init__(self, *args, **kwargs):
        super(NagiosPluginSNMP, self).__init__(*args, **kwargs)

        self.snmp_version = 0

        if self.options.snmpv2:
            self.snmp_version = 1
        elif self.options.snmpv3:
            self.snmp_version = 2

        # Init a new probe of type SNMP
        self.snmp = ProbeSNMP(
            hostaddress=self.options.hostname,
            community=self.options.snmpcommunity,
            snmp_version=self.snmp_version,
            login=self.options.snmpv3_login,
            password=self.options.snmpv3_password,
            auth_protocol=self.options.auth_protocol,
            priv_protocol=self.options.priv_protocol,
        )

        if 'NagiosPluginSNMP' == self.__class__.__name__:
            logger.debug('=== END PLUGIN INIT ===')

    def define_plugin_arguments(self):
        """Define arguments for the plugin"""
        super(NagiosPluginSNMP, self).define_plugin_arguments()

        # Add common arguments
        self.required_args.add_argument('-C',
                                        dest='snmpcommunity',
                                        help='SNMP Community to use')
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

        # Specific to SNMPv3
        self.parser.add_argument('-3',
                                 action='store_true',
                                 dest='snmpv3',
                                 default=False,
                                 help='Use SNMP v3 (default use version 1)')

        self.parser.add_argument('--login',
                                 dest='snmpv3_login',
                                 help='SNMPv3 login')

        self.parser.add_argument('--password',
                                 dest='snmpv3_password',
                                 help='SNMPv3 password')

        self.parser.add_argument('--auth-protocol',
                                 type=argument.snmpv3_auth_protocol,
                                 help='SNMPv3 authentication protocol')

        self.parser.add_argument('--priv-protocol',
                                 type=argument.snmpv3_priv_protocol,
                                 help='SNMPv3 priv protocol (encryption)')

    def verify_plugin_arguments(self):
        super(NagiosPluginSNMP, self).verify_plugin_arguments()

        if not self.options.snmpv3:
            if not self.options.snmpcommunity:
                self.unknown("Missing community string with -C argument !")

        if self.options.snmpv3:
            if not self.options.snmpv3_login \
               or not self.options.snmpv3_password:
                self.unknown("Login / Password required for SNMPv3 !")

