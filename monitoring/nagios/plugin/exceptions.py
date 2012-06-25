# -*- coding: utf-8 -*-
#===============================================================================
# Filename        : exceptions
# Author        : Vincent BESANCON aka 'v!nZ' <besancon.vincent@gmail.com>
# Description   : Define class for Nagios events and plugin exceptions.
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


class NagiosCritical(Exception):
    """Raise to fire a CRITICAL event to Nagios and stop plugin execution.
    
    :param msg: Output message in Nagios
    :type msg: string
    """
    
    def __init__(self, msg):
        print "CRITICAL - %s" % msg
        raise SystemExit(2)

class NagiosWarning(Exception):
    """Raise to fire a WARNING event to Nagios and stop plugin execution.
    
    :param msg: Output message in Nagios
    :type msg: string
    """
    
    def __init__(self, msg):
        print "WARNING - %s" % msg
        raise SystemExit(1)

class NagiosUnknown(Exception):
    """Raise to fire a UNKNOWN event to Nagios and stop plugin execution.
    
    :param msg: Output message in Nagios
    :type msg: string
    """
    
    def __init__(self, msg):
        print "UNKNOWN - %s" % msg
        raise SystemExit(3)

class NagiosOk(Exception):
    """Raise to fire a OK event to Nagios and stop plugin execution.
    
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