#===============================================================================
# -*- coding: UTF-8 -*-
# Module        : exceptions
# Author        : Vincent BESANCON aka 'v!nZ' <besancon.vincent@gmail.com>
# Description   : Define class for Nagios events exceptions.
#-------------------------------------------------------------------------------
# This file is part of NagiosPPT (Nagios Python Plugin Template).
#
# NagiosPPT is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NagiosPPT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NagiosPPT.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

""":mod:`nagppt.exceptions` -- This module define class for Nagios events exceptions"""

class NagiosCritical(Exception):
    """Raise to fire a CRITICAL event to Nagios and stop plugin execution.
    
    :param msg: Output message in Nagios
    :type msg: string
    
    **Usage**:
    
    .. sourcecode:: python
     
     from nagppt.exceptions import NagiosCritical
     raise NagiosCritical("Cannot connect to database !")
    
    This will make Nagios show a CRITICAL event with following output::
    
     CRITICAL - Cannot connect to database !
     
    .. note::
      The plugin will be stopped after raising exception !
    """
    
    def __init__(self, msg):
        print "CRITICAL - %s" % msg
        raise SystemExit(2)

class NagiosWarning(Exception):
    """Raise to fire a WARNING event to Nagios and stop plugin execution.
    
    :param msg: Output message in Nagios
    :type msg: string
    
    **Usage**:
    
    .. sourcecode:: python
     
     from nagppt.exceptions import NagiosWarning
     raise NagiosWarning("Free space available is low !")
    
    This will make Nagios show a WARNING event with following output::
    
     WARNING - Free space available is low !
     
    .. note::
      The plugin will be stopped after raising exception !
    """
    
    def __init__(self, msg):
        print "WARNING - %s" % msg
        raise SystemExit(1)

class NagiosUnknown(Exception):
    """Raise to fire a UNKNOWN event to Nagios and stop plugin execution.
    
    :param msg: Output message in Nagios
    :type msg: string
    
    **Usage**:
    
    .. sourcecode:: python
     
     from nagppt.exceptions import NagiosUnknown
     raise NagiosUnknown("Missing mandatory argument 'hostname !")
    
    This will make Nagios show a UNKNOWN event with following output::
    
     UNKNOWN - Missing mandatory argument 'hostname !
     
    .. note::
      The plugin will be stopped after raising exception !
    """
    
    def __init__(self, msg):
        print "UNKNOWN - %s" % msg
        raise SystemExit(3)

class NagiosOk(Exception):
    """Raise to fire a OK event to Nagios and stop plugin execution.
    
    :param msg: Output message in Nagios
    :type msg: string
    
    **Usage**:
    
    .. sourcecode:: python
     
     from nagppt.exceptions import NagiosOk
     raise NagiosOk("Everything is fine.")
    
    This will make Nagios show a OK event with following output::
    
     OK - Everything is fine.
     
    .. note::
      The plugin will be stopped after raising exception !
    """
    
    def __init__(self, msg):
        print "OK - %s" % msg
        raise SystemExit(0)