# -*- coding: UTF-8 -*-
#===============================================================================
# Filename      : definition.py
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

import logging as log
import os

logger = log.getLogger('monitoring.nagios.definition')

class ObjectDefinition(object):
    """
    Class that define a Nagios object definition.
    """
    def __init__(self, options):
        self.templates = []
        self.customs = {}

        self.__process_options(options)

    # Public
    def get_templates(self):
        """
        Get templates from use option.
        """
        if hasattr(self, 'use'):
            use = self.use.split(',')
            use_cleaned = []
            for entry in use:
                use_cleaned.append(entry.strip())
            return use_cleaned
        else:
            return []

    def is_template(self):
        """
        Return True if object is a template or False if not.
        """
        try:
            return self.register == '0'
        except AttributeError:
            return False

    def get_inherited_templates(self):
        for obj in self.templates:
            print "%s" % obj
            if len(obj.templates) > 0:
                obj.get_inherited_templates()

    # Private
    def __process_options(self, options):
        """
        Processing options during instance initialization.
        """
        for key in options:
            # Option is a custom variable
            if key[0] == '_':
                custom_var_name = key.upper()
                self.customs[custom_var_name] = options[key]
            else:
                # Create the attribute for this option
                setattr(self, key, options[key])

class ObjectGroup(object):
    """
    Class that act on a group of Nagios object (all hosts, all services...).
    """
    def __init__(self, objects):
        self.objects = objects
        self.templates = []

        self.__create_available_templates()
        self.__create_templates_dependencies()

    # Public
    def render_templates_graph(self, root='', filename=os.path.expanduser('~/templates.svg'), layout='twopi'):
        """
        Render the graph of templates. Output format depends on the file extension.
        Could be svg, png, jpg.
        """
        try:
            import pygraphviz as pgv
        except ImportError:
            logger.critical('You need pygraphviz and graphviz to render templates graph !')
            raise SystemExit()

        logger.info('Generating the graph.')

        G = pgv.AGraph(strict=False, directed=True)
        G.graph_attr['root'] = root
        G.graph_attr['size'] = '10,15'
        G.graph_attr['page'] = '11.69,16.54'
        G.graph_attr['margin'] = '0.69,0.54'
        G.node_attr['shape'] = 'none'
        G.graph_attr['ranksep'] = '10'
        G.node_attr['fontsize'] = '22.0'

        # Add all nodes (all templates)
        for tpl in self.templates:
            G.add_node(tpl)
        # Add all edges (link between them)
        for tpl in self.templates:
            for father in tpl.templates:
                G.add_edge(father, tpl)

        logger.info('Exporting to file: %s' % filename)
        G.draw(filename, prog=layout)

    # Private
    def __create_available_templates(self):
        """
        Create the list of available templates.
        """
        for obj in self:
            if obj.is_template():
                self.templates.append(obj)

    def __find_tpl_by_name(self, name):
        """
        Find a Template by name. Return a Python Object representation of the Nagios one.
        """
        logger.debug('Trying to find template %s by name.' % name)
        for obj in self.templates:
            if hasattr(obj, 'name') and obj.name == name:
                return obj
        return None

    def __create_templates_dependencies(self):
        """
        Create the templates dependencies for each object definitions.
        """
        # For each object def create the list of templates that it uses but in Pythonic way
        for obj in self:
            templates = obj.get_templates()
            object_templates = []
            for tpl in templates:
                tpl_obj = self.__find_tpl_by_name(tpl)
                if tpl_obj is not None:
                    object_templates.append(tpl_obj)
                else:
                    logger.critical('Template %s is not defined !' % tpl)
            obj.templates = object_templates

    # Specials methods
    def __iter__(self):
        return self.objects.__iter__()

    def __getitem__(self, key):
        return self.objects[key]
