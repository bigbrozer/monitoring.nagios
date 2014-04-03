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
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

from monitoring.nagios.probes import Probe
from monitoring.nagios.exceptions import NagiosUnknown

logger = logging.getLogger('monitoring.nagios.probes.http')


class HTTPResponse(object):
    """
    This class represents the HTTP response from the server.

    This is a wrapper arround ``requests.Response`` object with extensions like
    parsing response to others formats.

    Check out `requests.Response API reference <http://www.python-requests.org/en/latest/api/#requests.Response>`_ for more details.
    """
    __attributes = ()

    def __init__(self, response):
        self.__response = response

    def __getattr__(self, item):
        """
        Basic wrapper for getting attributes of ``HTTPResponse`` and
        ``requests.Response`` objects.
        """
        if item in self.__attributes:
            return getattr(self, item)
        else:
            return getattr(self.__response, item)

    def xml(self):
        """
        Parse response as XML and make a BeautifulSoup out of it.

        :returns: an instance of ``BeautifulSoup`` class.
        """
        if self.status_code == ProbeHTTP.status_codes.ok:
            xml = BeautifulSoup(self.text)
            if xml.find_all(True):
                return xml
            else:
                raise NagiosUnknown("Cannot parse XML data ! "
                                    "Please investigate.")
        else:
            raise NagiosUnknown(
                "HTTP Error {0.status_code}: Unable to fetch "
                "XML data from {0.url} !".format(self))


class ProbeHTTP(Probe):
    """
    An HTTP probe doing HTTP GET/POST request from your plugins.

    This is basically just a wrapper arround `requests
    <http://www.python-requests.org/en/latest/>`_ library.
    """
    status_codes = requests.codes

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
        url = "{0}/{1}".format(self.baseurl, path)

        try:
            response = requests.get(url, auth=self.auth, **kwargs)
            response.raise_for_status()
        except RequestException as e:
            raise NagiosUnknown("HTTP GET error on URL: {}\n"
                                "{}".format(url, e))

        return HTTPResponse(response)

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
        url = "{0}/{1}".format(self.baseurl, path)

        try:
            response = requests.post(url, data, auth=self.auth, **kwargs)
        except RequestException as e:
            raise NagiosUnknown("HTTP POST error on URL: {}\n"
                                "{}".format(url, e))

        return HTTPResponse(response)