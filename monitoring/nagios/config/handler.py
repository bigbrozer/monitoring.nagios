# -*- coding: utf-8 -*-
#===============================================================================
# Filename      : handler
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
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

"""
This module provides classes to handle the Nagios configuration.
"""

import logging as log

# Imports from Python Standard library
import os, re
from ConfigParser import ConfigParser, Error
from StringIO import StringIO

# Imports from monitoring.nagios library
from monitoring.nagios.config.exceptions import SettingsFileError
from monitoring.nagios.objects.hosts import Host, Hosts
from monitoring.nagios.objects.hostgroups import Hostgroup, Hostgroups
from monitoring.nagios.objects.services import Service, Services

logger = log.getLogger('monitoring.nagios.config')


# Configure "from ... import *"
__all__ = ['ConfigFileHandler']


def logsection(line):
    """Format a nice log section."""
    return "==== {} ====".format(line).upper()


class ConfigFileHandler(object):
    """
    This class handles the Nagios configuration.
    """
    settings_file = os.path.expanduser('~/.monitoring')

    # Object Types - {'type': ('Class', 'GroupClass', 'Property')}
    object_types = {
        'host': (Host, Hosts, 'hosts'),
        'hostgroup': (Hostgroup, Hostgroups, 'hostgroups'),
        'hostdependency': '',
        'service': (Service, Services, 'services'),
        'servicegroup': '',
        'servicedependency': '',
        'command': '',
        'timeperiod': '',
        'contact': '',
        'contactgroup': '',
    }

    def __init__(self):
        logger.info('Initialize configuration.')
        self.total_files = 0
        self.config_root_dir = ""

        # Read settings file
        self.read_settings()

    def __list_files(self):
        """
        Method generator that walk in the config directory and returns the full
        path of a config file.

        :return: full path of a config file.
        :rtype: str, unicode
        """
        logger.debug('Configuration directory is \"%s\".' % self.config_root_dir)
        for root, lsdirs, lsfiles in os.walk(self.config_root_dir):
            for file in lsfiles:
                if re.search('.*\.cfg$', file):
                    fullpath = os.path.join(root, file)
                    self.total_files += 1
                    yield fullpath

    def _read_raw_config(self):
        """
        Return all Nagios object definitions as if we have only one **BIG** file
        containing all.
        """
        buffer = StringIO()

        logger.info(logsection('Configuration to raw objects'))
        logger.info('Reading configuration files...')
        for filename in self.__list_files():
            logger.debug('Reading file "%s".' % filename)
            buffer.write('\n')
            buffer.write('# IMPORTED FROM=%s\n' % filename)
            with open(filename, 'rU') as content:
                buffer.write(content.read())

        allinone_cfg = buffer.getvalue()
        buffer.close()

        logger.info('Done. Read %s file(s).' % self.total_files)
        return allinone_cfg

    def _read_raw_object(self, raw_config):
        """
        Parse Nagios configuration.

        Return each object as dict: ``{ 'type': [list_options] }`` with ``type``
        the name of the Nagios object type (eg. host) and ``list_options`` the
        list of dict for options in the object definition.

        :param raw_config: the StringIO containing the full Nagios configuration's definitions.
        :type raw_config: str, unicode
        """
        object_types = self.__class__.object_types

        logger.info(logsection('Parse configuration'))
        logger.info('Parsing the configuration and keep in global dict all options about definitions...')

        objects = {}
        for t in object_types.keys():
            objects[t] = []
        options = {}
        in_define = False
        continuation_line = False
        current_object_type = ""
        single_line = ""
        from_file = ""

        for line in raw_config.split('\n'):
            define_line = re.match(r'^define\s+(\w+)', line)
            define_end_line = re.search(r'}', line)

            # Detect where is the file defining this object
            if line.startswith('# IMPORTED FROM='):
                from_file = line.split('=')[1]

            # Entering definition
            if define_line:
                in_define = True
                options = {}
                current_object_type = define_line.group(1)
                logger.debug("Entering %s object definition..." % current_object_type)
                continue

            # We are inside a definition
            if in_define:
                if re.match(r'.*\\\s*$', line):
                    # The line continue on next line, put on single line
                    logger.debug("The line has \'\\\'...")
                    continuation_line = True
                    line = re.sub(r"\s*\\\s*$", "", line)
                    line = re.sub(r"^\s*", "", line)
                    single_line += line
                    continue
                elif continuation_line:
                    # Now the continuation line is complete
                    logger.debug("The continuation line is complete.")
                    continuation_line = False
                    line = re.sub("^\s*", "", line)
                    line = single_line + line
                    single_line = ""

                option_line = re.match(r'^\s*([a-zA-Z0-9_-]+)\s+(.*)$', line)
                if option_line:
                    # Parse the option line
                    name = option_line.group(1)
                    value = option_line.group(2)
                    options[name] = value
                    options['from_file'] = from_file

                    logger.debug('\tReading option %s, with value: %s' % (name, value))
                    continue

            # Exiting definition
            if define_end_line:
                in_define = False
                objects[current_object_type].append(options)
                logger.debug("Leaving object definition...")
                continue

        return objects

    def _create_objects(self, raw_objects, nagios_type):
        """
        Create Python objects from Nagios one.
        """
        logger.info('Creating Python objects for %s.' % nagios_type)

        object_types = self.__class__.object_types
        (cls, clss, prop) = object_types[nagios_type]

        list_obj = []
        for nagios_obj in raw_objects[nagios_type]:
            python_obj = cls(nagios_obj)
            list_obj.append(python_obj)

        setattr(self, prop, clss(list_obj))

    def read_settings(self):
        """
        Read the settings file and set some attributes.
        Actually find the location of Nagios configuration.
        """
        settings_file = self.__class__.settings_file

        # Init settings
        logger.info('Reading settings file \'%s\'.' % settings_file)
        self.__settings = ConfigParser()

        # Find config directory in settings file
        try:
            self.__settings.read(settings_file)
            self.config_root_dir = self.__settings.get('svn', 'basedir')
        except Error as e:
            logger.critical('Error: cannot parse settings file \'%s\' !' % settings_file)
            logger.critical('\tMessage: %s' % e)
            raise SettingsFileError()

    def read_config(self):
        """
        Read and parse the Nagios Configuration. Create Python objects.
        """
        raw_config = self._read_raw_config()
        raw_objects = self._read_raw_object(raw_config)

        self._create_objects(raw_objects, 'host')
        self._create_objects(raw_objects, 'service')


if __name__ == '__main__':
    logger = log.getLogger('test')

    if os.environ.get('MONLIB_DEBUG') == 'true':
        logger.setLevel(log.DEBUG)

    cfg = ConfigFileHandler()
    raw_config = cfg._read_raw_config()
    raw_objects = cfg._read_raw_object(raw_config)

    cfg._create_objects(raw_objects, 'service')