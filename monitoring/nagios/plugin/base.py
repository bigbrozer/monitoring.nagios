# -*- coding: UTF-8 -*-
#
#===============================================================================
# Name          : base
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : Base class for developing new Nagios Plugins.
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

import argparse
import logging as log

from monitoring.nagios.plugin.exceptions import NagiosUnknown

#-------------------------------------------------------------------------------
# Class that define the default Nagios plugin structure
#-------------------------------------------------------------------------------
#
class NagiosPlugin(object):
    def __init__(self, name, version, description):
        """Initialize a new Nagios Plugin"""
        self.log = log.getLogger('nagios.plugin.base')

        self.pluginname = name
        self.pluginversion = version
        self.plugindesc = description

        # Initialize arguments stuff
        self._init_plugin_arguments()
        self.define_plugin_arguments()
        self._parse_plugin_arguments()
        self.verify_plugin_arguments()
        
        # Check if debug mode is active
        if self.options.debug:
            self.log.setLevel(log.DEBUG)
        
        # Debug
        self.log.debug('Debug mode is ON.')
        self.log.debug('Plugin class: %s.' % self.__class__.__name__)
        self.log.debug('\tName: %s, v%s' % (self.pluginname, self.pluginversion))
        self.log.debug('\tDesc: %s' % self.plugindesc)
        self.log.debug('Arguments passed on command line %s.' % vars(self.options))

    # Arguments processing
    def _init_plugin_arguments(self):
        """
        Initialize the argument parser.
        """
        self.parser = argparse.ArgumentParser(description=self.plugindesc)
        self.parser.add_argument('--debug', action='store_true', dest='debug', help='Show debug information, Nagios may truncate output')
        self.parser.add_argument('--version', action='version', version='%s %s' % (self.parser.prog, self.pluginversion))

        self.required_args = self.parser.add_argument_group('required arguments')

    def define_plugin_arguments(self):
        """
        Define arguments for the plugin, override this method to include yours.
        """
        self.required_args.add_argument('-H', dest='hostname', help='Target hostname (FQDN or IP address)', required=True)

    def verify_plugin_arguments(self):
        """
        Check syntax of all arguments, override this method to include yours.
        """
        if not self.options.hostname:
            raise NagiosUnknown('Missing host information ! (option -H)')

    def _parse_plugin_arguments(self):
        """
        Parse arguments and values.
        """
        self.options = self.parser.parse_args()

if __name__ == '__main__':
    from monitoring.log import mainlog
    mainlog.info('Creating instance of the plugin.')
    plugin = NagiosPlugin("hello", "1.0", "Just a test")
    mainlog.info('Done.')