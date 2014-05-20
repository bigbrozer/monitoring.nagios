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

"""
This module contains a set of functions to convert or specify argument types.

See ``type`` argument of `argparse's add_argument()
<http://docs.python.org/2/library/argparse.html#type>`_ module.
"""

import argparse
import re
from datetime import timedelta

from pysnmp.entity.rfc3413.oneliner import cmdgen


def snmpv3_auth_protocol(protocol):
    """
    Specify a SNMPv3 auth protocol to use for the connection.

    :param protocol: the name of the protocol for authentication.
                     Checkout `PySNMP Security Reference
                     <http://pysnmp.sourceforge.net/docs/current/security-configuration.html>`_
    :type protocol: str, unicode
    :returns: the SNMPv3 USM class for the protocol.

    **Example**::

     >>> p = snmpv3_auth_protocol("md5")
     >>> type(p)
     <type 'tuple'>
     >>> snmpv3_auth_protocol("md5ufdk")
     Traceback (most recent call last):
       ...
     ArgumentTypeError: Unsupported auth protocol 'md5ufdk' ! Supported are md5, noauth, sha.
    """

    # Lookup table for SNMPv3 auth protocols
    #
    # usmHMACMD5AuthProtocol    -- MD5-based authentication protocol
    # usmHMACSHAAuthProtocol    -- SHA-based authentication protocol
    # usmNoAuthProtocol         -- no authentication to use
    #
    snmpv3_auth_protocols = {
        "md5": cmdgen.usmHMACMD5AuthProtocol,
        "sha": cmdgen.usmHMACSHAAuthProtocol,
        "noauth": cmdgen.usmNoAuthProtocol,
    }

    try:
        return snmpv3_auth_protocols[protocol]
    except KeyError as e:
        raise argparse.ArgumentTypeError(
            "Unsupported auth protocol {} ! Supported are {}.".format(
                e, ", ".join(sorted(snmpv3_auth_protocols.keys()))))


def snmpv3_priv_protocol(protocol):
    """
    Specify a SNMPv3 priv protocol to use for the encryption.

    :param protocol: the name of the privacy protocol for encryption.
                     Checkout `PySNMP Security Reference
                     <http://pysnmp.sourceforge.net/docs/current/security-configuration.html>`_
    :type protocol: str, unicode
    :returns: the SNMPv3 USM class for the protocol.

    **Example**::

     >>> p = snmpv3_priv_protocol("des")
     >>> type(p)
     <type 'tuple'>
     >>> snmpv3_priv_protocol("desjfi")
     Traceback (most recent call last):
       ...
     ArgumentTypeError: Unsupported priv protocol 'desjfi' ! Supported are 3des, aes128, aes192, aes256, des, nopriv.
    """

    # Lookup table for SNMPv3 priv protocols (encryption)
    #
    # usmDESPrivProtocol        -- DES-based encryption protocol
    # usmAesCfb128Protocol      -- AES128-based encryption protocol (RFC3826)
    # usm3DESEDEPrivProtocol    -- triple DES-based encryption protocol
    # usmAesCfb192Protocol      -- AES192-based encryption protocol
    # usmAesCfb256Protocol      -- AES256-based encryption protocol
    # usmNoPrivProtocol         -- no encryption to use
    #
    snmpv3_priv_protocols = {
        "des": cmdgen.usmDESPrivProtocol,
        "aes128": cmdgen.usmAesCfb128Protocol,
        "3des": cmdgen.usm3DESEDEPrivProtocol,
        "aes192": cmdgen.usmAesCfb192Protocol,
        "aes256": cmdgen.usmAesCfb256Protocol,
        "nopriv": cmdgen.usmNoPrivProtocol,
    }

    try:
        return snmpv3_priv_protocols[protocol]
    except KeyError as e:
        raise argparse.ArgumentTypeError(
            "Unsupported priv protocol {} ! Supported are {}.".format(
                e, ", ".join(sorted(snmpv3_priv_protocols.keys()))))


def http_basic_auth(auth_string):
    """
    Convert a HTTP Basic Authentication string to a tuple.

    :param auth_string: the basic auth string of the form ``login:passwd``.
    :type auth_string: str, unicode
    :returns: Basic auth as a tuple ``(login, passwd)``.
    :rtype: tuple

    **Example**::

     >>> http_basic_auth("besancon:8jj_767hhgy")
     ('besancon', '8jj_767hhgy')
    """
    return tuple(auth_string.split(":"))


def days(integer):
    """
    Convert ``integer`` to a timedelta object. ``integer`` is a number of days.

    :param integer: the number of days.
    :type integer: str, unicode
    :return: the number of days as a timedelta object.
    :rtype: timedelta

    **Example**::

     >>> days(5)
     datetime.timedelta(5)
    """
    return timedelta(days=int(integer))


def hours(integer):
    """
    Convert ``integer`` to a timedelta object.

    Argument ``integer`` is a number of hours.

    :param integer: the number of hours.
    :type integer: str, unicode
    :return: the number of hours as a timedelta object.
    :rtype: timedelta

    **Example**::

     >>> hours(4)
     datetime.timedelta(0, 14400)
    """
    return timedelta(hours=int(integer))


def minutes(integer):
    """
    Convert ``integer`` to a timedelta object. ``integer`` is a number of
    minutes.

    :param integer: the number of minutes.
    :type integer: str, unicode
    :return: the number of minutes as a timedelta object.
    :rtype: timedelta

    **Example**::

     >>> minutes(32)
     datetime.timedelta(0, 1920)
    """
    return timedelta(minutes=int(integer))


def seconds(integer):
    """
    Convert ``integer`` to a timedelta object. ``integer`` is a number of
    seconds.

    :param integer: the number of seconds.
    :type integer: str, unicode
    :return: the number of seconds as a timedelta object.
    :rtype: timedelta

    **Example**::

     >>> seconds(54)
     datetime.timedelta(0, 54)
    """
    return timedelta(seconds=int(integer))


def percent(integer):
    """
    Check that ``integer`` is in range [0, 100] and returns the integer value.

    :param integer: an integer for percent value.
    :type integer: int
    :return: ``integer`` if in range [0, 100].
    :rtype: int

    :raises: argparse.ArgumentTypeError

    **Example**::

     >>> percent(54)
     54
     >>> try:
     ...    percent(234)
     ... except argparse.ArgumentTypeError as e:
     ...    e.message
     'Must be a percent value between [0, 100] !'
    """
    if integer in xrange(0, 100):
        return integer
    else:
        raise argparse.ArgumentTypeError("Must be a percent value between "
                                         "[0, 100] !")


class NagiosThreshold(object):
    """
    This class represents a Nagios threshold as defined in the
    `Guidelines for Developers
    <https://nagios-plugins.org/doc/guidelines.html#THRESHOLDFORMAT>`_.

    The ``threshold`` format is the following to make it simple:
    ``[@]start[:end]``. If ``start`` is ``~``, it means negative infinity.

    :param threshold: the Nagios threshold (ex. start:end, @start:end,
                      ...). With ``start`` and ``end`` as integer.
    :type threshold: str, unicode

    >>> t = NagiosThreshold("@25:40")
    >>> t.test(10) # OK: outside the range of {25 .. 40}
    False
    >>> t.test(30) # KO: inside the range of {25 .. 40}
    True
    >>> str(t)
    '[25 .. 40]'

    >>> t = NagiosThreshold("30")
    >>> t.test(40) # KO: outside the range of {0 .. 30}
    True
    >>> t.test(10) # OK: inside the range of {0 .. 30}
    False
    >>> t.test(-10) # KO: outside the range of {0 .. 30}
    True
    >>> str(t)
    '< 0 or > 30'

    >>> t = NagiosThreshold("~:20")
    >>> t.test(30) # KO: outside the range of {-∞ .. 20}
    True
    >>> t.test(15) # OK: inside the range of {-∞ .. 20}
    False
    >>> str(t)
    '> 20'

    >>> t = NagiosThreshold("10:20")
    >>> t.test(30) # KO: outside the range of {10 .. 20}
    True
    >>> t.test(13) # OK: inside the range of {10 .. 20}
    False
    >>> str(t)
    '< 10 or > 20'
    """
    pattern = r'(^(?P<inclusive>@)?(?P<start>[0-9]+)|' \
              r'(?P<is_strict_positive>^~)):?(?P<end>[0-9]*)$'

    def __init__(self, threshold):
        self.threshold = threshold
        self.__match = re.match(self.pattern, self.threshold)
        self.inclusive = False
        self.start = 0
        self.end = 0
        self.is_strict_positive = False

        if self.__match:
            # Set attributes
            attributes = self.__match.groupdict()

            if attributes["inclusive"]:
                self.inclusive = True

            if attributes["start"]:
                self.start = int(attributes["start"])

            if attributes["end"]:
                self.end = int(attributes["end"])

            if attributes["is_strict_positive"]:
                self.is_strict_positive = True

            # Sanity checks
            if self.start and self.end:
                if not self.start <= self.end:
                    raise argparse.ArgumentTypeError("Error: "
                                                     "start must be <= end !")
        else:
            raise argparse.ArgumentTypeError(
                "Threshold \"{0.threshold}\" does not "
                "match \"{0.pattern}\" !".format(self))

    def test(self, value):
        """
        Test ``value`` against threshold to know if an alert must be
        generated. If the test pass, it returns True to tell an alert is
        needed.

        It makes it easy from plugin arguments to test a value now::

         value = 54
         if plugin.options.warning.test(value):
            # Create an alert
            plugin.warning("A warning here !")
         elif plugin.options.critical.test(value):
            # Create an alert
            plugin.critical("Critical alert !!")
         else:
            plugin.ok("Nothing is going wrong here.")

        :param value: the value that must be tested on the threshold.
        :type value: int
        :returns: returns True if alert must be generated else False.
        """
        if self.is_strict_positive:
            if value > self.end:
                return True
        else:
            if self.inclusive:
                if self.start <= value <= self.end:
                    return True
            else:
                if self.start and not self.end:
                    if value > self.start or value < 0:
                        return True
                else:
                    if value < self.start or value > self.end:
                        return True

        return False

    def __str__(self):
        if self.is_strict_positive:
            return "> {0.end}".format(self)
        else:
            if self.inclusive:
                return "[{0.start} .. {0.end}]".format(self)
            else:
                if self.start and not self.end:
                    return "< 0 or > {0.start}".format(self)
                else:
                    return "< {0.start} or > {0.end}".format(self)
