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

import sys
import os
import argparse
import logging as log

from monitoring.nagios.plugin.exceptions import NagiosUnknown, NagiosCritical, NagiosWarning, NagiosOk

logger = log.getLogger('monitoring.nagios.plugin.base')

#-------------------------------------------------------------------------------
# Class that define the default Nagios plugin structure
#-------------------------------------------------------------------------------
#
class NagiosPlugin(object):
    """
    Create a new Nagios plugin.

    You may inherit from this class if you want to configure default behavior.
    """

    def __init__(self, name=os.path.basename(sys.argv[0]), version='', description=''):
        """
        Initialize a new Nagios Plugin.

        Please avoid to override __init__ in derived classes. See :function:`initialize` to do this.
        """
        self.name = name
        self.version = version
        self.description = description

        # Initialize arguments stuff
        self.__init_plugin_arguments()
        self.define_plugin_arguments()
        self.__parse_plugin_arguments()

        # Check if debug mode is active
        if self.options.debug:
            # Set monitoring logger option
            log.getLogger('plugin').setLevel(log.DEBUG)
            log.getLogger('monitoring').setLevel(log.DEBUG)

        # Debug init
        logger.debug('Debug mode is ON.')
        logger.debug('Plugin class: %s.' % self.__class__.__name__)
        logger.debug('\tName: %s, v%s' % (self.name, self.version))
        logger.debug('\tDesc: %s' % self.description)
        logger.debug('Arguments passed on command line %s.' % vars(self.options))

        # Sanity checks for plugin arguments
        self.verify_plugin_arguments()

        # Second level of initialization
        self.initialize()

    def initialize(self):
        """
        Second level of initialization.

        Overrides this method if you need to init some attributes after __init__.
        Do the same things but at plugin level.
        """
        logger.debug('Calling initialize...')

    # Arguments processing
    def __init_plugin_arguments(self):
        """
        Initialize the argument parser.
        """
        self.parser = argparse.ArgumentParser(description=self.description)
        self.parser.add_argument('--debug', action='store_true', dest='debug', help='Show debug information, Nagios may truncate output')
        self.parser.add_argument('--version', action='version', version='%s %s' % (self.parser.prog, self.version))

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

    def __parse_plugin_arguments(self):
        """
        Parse arguments and values.
        """
        self.options = self.parser.parse_args()

    # Nagios status methods
    def ok(self, msg):
        raise NagiosOk(msg)

    def warning(self, msg):
        raise NagiosWarning(msg)

    def critical(self, msg):
        raise NagiosCritical(msg)

    def unknown(self, msg):
        raise NagiosUnknown(msg)
