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
import traceback
import pickle
from pprint import pformat
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
        logger.debug('=== BEGIN PLUGIN INIT ===')
        logger.debug('Debug mode is ON.')
        logger.debug('Plugin class: %s.' % self.__class__.__name__)
        logger.debug('\tName: %s, v%s' % (self.name, self.version))
        logger.debug('\tDesc: %s' % self.description)
        logger.debug('Processed command line arguments:')
        logger.debug(pformat(vars(self.options), indent=4))

        # Pickle file name
        self.picklefile = '/var/tmp/{plugin.name}_{opt.hostname}.pkl'.format(plugin=self, opt=self.options)

        # Sanity checks for plugin arguments
        self.verify_plugin_arguments()

        # Second level of initialization
        self.initialize()

        if 'NagiosPlugin' == self.__class__.__name__: logger.debug('=== END PLUGIN INIT ===')

    def initialize(self):
        """
        Second level of initialization.

        Overrides this method if you need to init some attributes after __init__.
        Do the same things but at plugin level.
        """
        logger.debug('Calling second level of initialization.')

    # Arguments processing
    def __init_plugin_arguments(self):
        """
        Initialize the argument parser.
        """
        self.parser = argparse.ArgumentParser(description=self.description)
        self.parser.add_argument('--debug', action='store_true', dest='debug', help='Show debug information, Nagios may truncate output')
        self.parser.add_argument('--version', action='version', version='%s %s' % (self.parser.prog, self.version))

        self.required_args = self.parser.add_argument_group('Plugin arguments', 'This arguments are required by the plugin.')

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

    def load_data(self):
        """
        Load pickled data.

        :return: list
        :raise IOError: raise IOError if pickle file is not found / readable.
        """
        logger.debug('-- Try to find pickle file \'%s\'...' % self.picklefile)

        if os.path.isfile(self.picklefile):
            logger.debug('\t - Pickle file is found, processing.')
            data = list()
            try:
                with open(self.picklefile, 'rb') as pkl:
                    data = pickle.load(pkl)
            except (IOError, IndexError):
                message = """Unable to read retention file !
If you see this message that would mean that the retention file located in \'%s\' does not exists or it is not
readable. Check permissions or try to delete it to generate a new one. It may be possible that this version of this
plugin has changed and the retention file is outdated, so delete it if this is the case.

%s
""" % (self.picklefile, traceback.format_exc(limit=1))
                self.unknown(message)

            logger.debug('\t - Pickle data found, loading %d records.' % len(data))
            return data
        else:
            logger.debug('\t - No pickle file to load, continue.')
            raise IOError('Pickle file not found. You may save something first.')

    def save_data(self, data, limit=100):
        """
        Save data into a pickle file.

        :param data: A list of objects to save in the pickle file.
        :type data: list
        """
        logger.debug('-- Saving data to file \'%s\'...' % self.picklefile)
        try:
            # Avoid having a large pickle file if above 100 recorded values (plugin executions)
            if limit:
                while len(data) > limit:
                    logger.debug('\t - Records limit reached, purging old records.')
                    del data[0]

            # Save data with pickle module
            with open(self.picklefile, 'wb') as pkl:
                pickle.dump(data, pkl)
        except IOError:
            message = """Unable to save retention file !
If you see this message that would mean that the retention file located in \'%s\' is not writable. Check permissions.

%s
""" % (self.picklefile, traceback.format_exc(limit=1))
            self.unknown(message)

    # Nagios status methods
    def ok(self, msg):
        raise NagiosOk(msg)

    def warning(self, msg):
        raise NagiosWarning(msg)

    def critical(self, msg):
        raise NagiosCritical(msg)

    def unknown(self, msg):
        raise NagiosUnknown(msg)
