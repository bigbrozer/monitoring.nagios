# -*- coding: UTF-8 -*-
#===============================================================================
# Filename      : config.py
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

import os
import re
import logging as log
from StringIO import StringIO

from monitoring.nagios.objects.hosts import Host, Hosts

class Config(object):
    """
    This class handles the Nagios configuration.
    """
    # Locations of Nagios config repositories
    config_paths = (
        '/home/besancon/Repos/svn/trunk/dc_global',
        '/home/besancon/Repos/svn/trunk/dc_local',
        '/home/besancon/Repos/svn/trunk/dc_features',
    )

    # Object Types - {'type': ('Class', 'GroupClass', 'Property')}
    object_types = {
        'host': (Host, Hosts, 'hosts'),
        'hostgroup': '',
        'service': '',
        'servicegroup': '',
        'contact': '',
        'contactgroup': '',
        'timeperiod': '',
        'hostdependency': '',
        'servicedependency': '',
        'command': '',
        'hostescalation': '',
        'serviceescalation': '',
    }
    
    def __init__(self):
        log.info('Init configuration.')
        self.num_files = 0

    def _filenames(self):
        """
        Method generator that returns the full path of a config file.
        """
        config_paths = self.__class__.config_paths
        for repository in config_paths:
            for root, dirs, files in os.walk(repository):
                for file in files:
                    if re.search('.*\.cfg$', file):
                        fullpath = os.path.join(root, file)
                        self.num_files += 1
                        yield fullpath

    def read_raw_config(self):
        """
        Return all Nagios configuration data like if we have only one BIG cfg file.
        """
        buffer = StringIO()

        for filename in self._filenames():
            log.debug('Reading file "%s".' % filename)
            buffer.write('\n')
            buffer.write('# IMPORTED FROM: %s\n' % filename)
            content = open(filename, 'rU')
            buffer.write(content.read())
            content.close()

        allinone_cfg = buffer.getvalue()
        buffer.close()

        log.info('Processed %s file(s).' % self.num_files)
        return allinone_cfg

    def read_config(self, raw_config):
        """
        Parse Nagios configuration and return all objects as a dict:
        { 'type': [List] } with type the name of the Nagios object type (host)
        and List the list of dict for options in the object definition.
        """
        object_types = self.__class__.object_types

        objects = {}
        for t in object_types.keys():
            objects[t] = []
        options = {}
        in_define = False
        current_object_type = ""

        for line in raw_config.split('\n'):
            define_line = re.match(r'^define\s+(\w+)', line)
            end_define = re.search("}", line)

            if end_define:
                in_define = False
                objects[current_object_type].append(options)
                log.debug("Leaving object definition...")
            elif define_line:
                in_define = True
                options = {}
                current_object_type = define_line.group(1)
                log.debug("Entering %s object definition..." % current_object_type)
            else:
                if in_define:
                    option_line = re.match(r'\s+([a-zA-Z0-9_-]+)\s+(.*)$', line)
                    if option_line:
                        name = option_line.group(1)
                        value = option_line.group(2)
                        options[name] = value

                        log.debug('\tReading option %s, with value: %s' % (name, value))

        return objects

    def create_objects(self, raw_objects, nagios_type):
        """
        Create Python objects from Nagios one.
        """
        log.info('Creating Python objects for %s.' % nagios_type)

        object_types = self.__class__.object_types
        (cls, clss, prop) = object_types[nagios_type]

        list_obj = []
        for nagios_obj in raw_objects[nagios_type]:
            python_obj = cls(nagios_obj)
            list_obj.append(python_obj)

        setattr(self, prop, clss(list_obj))
