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

import logging

from monitoring.nagios.plugin import NagiosPlugin
from monitoring.nagios.probes import ProbeHTTP
from monitoring.nagios.plugin import argument

logger = logging.getLogger("monitoring.nagios.plugin.http")


class NagiosPluginHTTP(NagiosPlugin):
    """
    Base plugin that makes HTTP requests.

    Make HTTP requests using attribute :attr:`http` which is an instance of
    :class:`monitoring.nagios.probes.http.ProbeHTTP`.

    Example::

     plugin = NagiosPluginHTTP()
     response = plugin.http.get("/test.html")
     print response.content, response.status_code

    The following arguments are pre-defined and accessible with attribute
    :attr:`options`:

    - ``-H``: :attr:`options.hostname`
    - ``-p, --port``: :attr:`options.port`
    - ``-S, --ssl``: :attr:`options.ssl`
    - ``-a, --auth``: :attr:`options.auth`
    """
    def __init__(self, *args, **kwargs):
        super(NagiosPluginHTTP, self).__init__(*args, **kwargs)

        self.http = ProbeHTTP(hostaddress=self.options.hostname,
                              port=self.options.port,
                              ssl=self.options.ssl,
                              auth=self.options.auth)

        if 'NagiosPluginHTTP' == self.__class__.__name__:
            logger.debug('=== END PLUGIN INIT ===')

    def define_plugin_arguments(self):
        """Define arguments for the plugin"""
        super(NagiosPluginHTTP, self).define_plugin_arguments()

        # Add extra arguments
        self.required_args.add_argument('-p', '--port',
                                        dest='port',
                                        help='HTTP port (default 80).',
                                        default=80)

        self.required_args.add_argument('-P', '--path',
                                        dest='path',
                                        help='The URL path relative to host.',
                                        default="/")

        self.required_args.add_argument('-S', '--ssl',
                                        dest='ssl',
                                        action="store_true",
                                        help='Use SSL (default no).',
                                        default=False)

        self.required_args.add_argument('-a', '--auth',
                                        dest='auth',
                                        type=argument.http_basic_auth,
                                        help='Login and password for Basic'
                                             'Authentication.',
                                        default=None)