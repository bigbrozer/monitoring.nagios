# -*- coding: UTF-8 -*-
#===============================================================================
# Filename      : log
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : Manipulate log file returned by Nagios verification action.
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

import re

# Exceptions
class NagiosLogIOError(Exception):
    """Triggered if there is a problem parsing the Nagios log file."""
    pass

# Classes
class Log(object):
    """This represents the Nagios log file as returned by nagverif.

       content attribute contains the full log file in memory.
    """

    def __init__(self, sat_alias):
        self.content = ""
        self.host_has_no_service = ""
        self.duplicates = ""
        self.errors = ""
        
        try:
            with open('log/nagdeploy_%s.log' % sat_alias, 'r') as self.logfile:
                self.content = self.logfile.read()
        except IOError as e:
            raise NagiosLogIOError("Error with the Nagios log file: %s" % e)

        self._parse_log()

    def _parse_log(self):
        self.host_has_no_service = "\n".join(re.findall(r"Warning: Host.*has no services associated with it!", self.content, re.MULTILINE))
        self.duplicates = "\n".join(re.findall(r"^Warning: Duplicate definition found for service.*", self.content, re.MULTILINE))
        self.errors = "\n".join(re.findall(r"^Error.*", self.content, re.MULTILINE))

if __name__ == '__main__':
    log = Log('nagios.frh.de.corp')
