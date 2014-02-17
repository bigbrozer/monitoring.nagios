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

"""HTTP probe module."""

import logging

import requests

from monitoring.nagios.probes import Probe


logger = logging.getLogger('monitoring.nagios.probes.http')


class ProbeHTTP(Probe):
    """
    An HTTP probe doing HTTP GET/POST request from your plugins.

    This is basically just a wrapper arround `requests
    <http://www.python-requests.org/en/latest/>`_ library.
    """
    def __init__(self, hostaddress, port=80, ssl=False, auth=None):
        super(ProbeHTTP, self).__init__()

        self.hostaddress = hostaddress
        self.port = 80 if not port else port
        self.auth = () if not auth else auth
        self.protocol = "http" if not ssl else "https"
        self.baseurl = "{0.protocol}://{0.hostaddress}:{0.port}".format(self)

        logger.debug("Initialized a new HTTP probe on %s.", self.baseurl)

    def get(self, path, **kwargs):
        """
        Send a HTTP GET request. See requests.get() api reference.

        :param path: the URL location. This is the part after the
                     ``hostaddress``.
        :type path: str, unicode
        :param kwargs: optional arguments that requests takes.
        :returns: return of :func:`requests.get`.
        """
        path = path.lstrip("/")
        return requests.get("{0}/{1}".format(self.baseurl, path),
                            **kwargs)

    def post(self, path, data, **kwargs):
        """
        Send a HTTP POST request. See requests.post() api reference.

        :param path: the URL location. This is the part after the
                     ``hostaddress``.
        :type path: str, unicode
        :param data: Dictionary, bytes, or file-like object to send in the body
                     of the Request.
        :param kwargs: optional arguments that requests takes.
        :returns: return of :func:`requests.get`.
        """
        path = path.lstrip("/")
        return requests.post("{0}/{1}".format(self.baseurl, path),
                             data,
                             **kwargs)