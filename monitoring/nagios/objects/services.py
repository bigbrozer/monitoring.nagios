# -*- coding: utf-8 -*-
#===============================================================================
# Filename      : services.py
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

from monitoring.nagios.objects.definition import ObjectDefinition, ObjectGroup

class Service(ObjectDefinition):
    """
    Represent a service definition.
    """

    def __init__(self, options):
        super(Service, self).__init__(options)

    def __str__(self):
        return self.get_name()

class Services(ObjectGroup):
    """
    Represent all services objects defined in the configuration.
    """

    def __init__(self, objects):
        super(Services, self).__init__(objects)
