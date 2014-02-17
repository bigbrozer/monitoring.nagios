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

"""Exceptions modules for all plugins."""


class NagiosCritical(Exception):
    """
    Raise to fire a CRITICAL event to Nagios and stop plugin execution.

    :param msg: Output message in Nagios
    :type msg: string
    """

    def __init__(self, msg):
        print "CRITICAL - %s" % msg
        raise SystemExit(2)


class NagiosWarning(Exception):
    """
    Raise to fire a WARNING event to Nagios and stop plugin execution.

    :param msg: Output message in Nagios
    :type msg: string
    """

    def __init__(self, msg):
        print "WARNING - %s" % msg
        raise SystemExit(1)


class NagiosUnknown(Exception):
    """
    Raise to fire a UNKNOWN event to Nagios and stop plugin execution.

    :param msg: Output message in Nagios
    :type msg: string
    """

    def __init__(self, msg):
        print "UNKNOWN - %s" % msg
        raise SystemExit(3)


class NagiosOk(Exception):
    """
    Raise to fire a OK event to Nagios and stop plugin execution.

    :param msg: Output message in Nagios
    :type msg: string
    """

    def __init__(self, msg):
        print "OK - %s" % msg
        raise SystemExit(0)


class PluginError(StandardError):
    """
    Exception when a plugin error occur.

    :param output: Message to show in Nagios status information output.
    :type output: str
    :param longoutput: Message to show in long output (extra infos).
    :type longoutput: str
    """
    def __init__(self, output, longoutput, *args, **kwargs):
        super(PluginError, self).__init__(*args, **kwargs)

        self.message = '%s\n%s' % (output, longoutput)

    def __str__(self):
        return self.message
