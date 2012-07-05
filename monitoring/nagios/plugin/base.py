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
    Initialize a new Nagios Plugin.

    Please avoid to override __init__ in derived classes. See :func:`initialize` to do this.

    :param name: the name of the plugin. This is set to the name of the file by default.
    :param version: the version of the plugin. Set it to anything you want.
    :type version: str, unicode
    :param description: a description of what is doing the plugin.
    :type description: str, unicode
    """

    def __init__(self, name=os.path.basename(sys.argv[0]), version='', description=''):
        # Plugin infos
        self.name = name
        self.version = version
        self.description = description

        # Output handling
        self._output = ""
        self.shortoutput = ""
        self.longoutput = []
        self.perfdata = []

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

        # Pickle file name path and default pattern
        self._picklefile_path = '/var/tmp'
        self._picklefile_name = '{plugin.name}_{opt.hostname}'.format(plugin=self, opt=self.options)
        self.picklefile_pattern = 'p'

        # Plugin initialization
        self.initialize()

        # Set the full pickle file name and path (can be modified in second level of init)
        self.picklefile = '{0}/{1}_{2}.pkl'.format(self._picklefile_path, self._picklefile_name,
                                                   self.picklefile_pattern)

        # Sanity checks for plugin arguments
        self.verify_plugin_arguments()

        if 'NagiosPlugin' == self.__class__.__name__: logger.debug('=== END PLUGIN INIT ===')

    def initialize(self):
        """
        Plugin level initialization.

        Overrides this method if you need to init some attributes after __init__. This avoid to ovverrides __init__
        in base class and also provide a way to init things before arguments sanity checks are run by
        :py:func:`verify_plugin_arguments`.
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
        try:
            self.options = self.parser.parse_args()
        except Exception as e:
            self.unknown('Error argument parser: %s' % e)

    def load_data(self):
        """
        Load pickled data.

        :return: list
        :raise IOError: raise IOError if pickle file is not found / readable.
        """
        logger.debug('-- Try to find pickle file \'%s\'...' % self.picklefile)

        data = None
        if os.path.isfile(self.picklefile):
            logger.debug('\t - Pickle file is found, processing.')
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

    def save_data(self, data, limit=0):
        """
        Save data into a pickle file.

        :param data: A list of objects to save in the pickle file.
        :type data: list
        """
        logger.debug('-- Saving data to file \'%s\'...' % self.picklefile)
        try:
            # Avoid having a large pickle file if above limit of recorded values (plugin executions)
            if limit and type(data) is list:
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

    def output(self, substitute=None, long_output_limit=20):
        """
        Construct and format the full string that should be returned to Nagios. Includes short output,
        long output and perf data (if any).

        :param substitute: dict wih key/value pair that should be replaced in string (see :py:func:`str.format`).
        :type substitute: dict
        :param long_output_limit: limit the number of lines of long output, default to ``20``. Set it to ``None`` for no limit.
        :type long_output_limit: int, None

        :return: str, unicode
        """
        if not substitute:
            substitute = {}

        self._output += "{0}".format(self.shortoutput)
        if self.longoutput:
            self._output = self._output.rstrip("\n")
            self._output += "\n{0}".format("\n".join(self.longoutput[:long_output_limit]))
            if long_output_limit:
                self._output += "\n(...showing only first {0} lines, {1} elements remaining...)".format(
                    long_output_limit,
                    len(self.longoutput[long_output_limit:])
                )
        if self.perfdata:
            self._output = self._output.rstrip("\n")
            self._output += " | {0}".format(" ".join(self.perfdata))
        return self._output.format(**substitute)

    # Nagios status methods
    def ok(self, msg):
        raise NagiosOk(msg)

    def warning(self, msg):
        raise NagiosWarning(msg)

    def critical(self, msg):
        raise NagiosCritical(msg)

    def unknown(self, msg):
        raise NagiosUnknown(msg)
