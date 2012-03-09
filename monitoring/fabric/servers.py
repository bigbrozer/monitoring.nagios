# -*- coding: UTF-8 -*-
#===============================================================================
# Filename      : servers
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : Define all servers we have in charge.
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

from fabric.api import env
from urllib import urlopen
import csv

def get_satellites_list():
    """
    Append to env.hosts[] the full list of Nagios satellites in production
    Exit with code 2 (CRITICAL like Nagios ;-)) if the URL cannot be retrieved.
    """
    url_sat_list = 'http://monitoring-dc.app.corp/optools/nagios/satellites/export/csv'
    satellites = []
    try:
        csv_sat_list = csv.reader(urlopen(url_sat_list), delimiter=';')
        for row in csv_sat_list:
            satellites.append(row[2])
        return satellites
    except:
        print 'Error: Unable to parse URL: %s !' % url_sat_list
        raise SystemExit(2)

#===============================================================================
# Define hosts list and roles
#===============================================================================
#
# -------
# Servers
# -------
#
env.roledefs = {
    'central'       : ['monitoring-dc.app.corp',],          # The central instance
    'admin'         : ['frseldev0002.sel.fr.corp',],        # Monitoring Admin Server
    'satellite_tpl' : ['frseltmp0001.sel.fr.corp',],        # Nagios Satellite Template
    'satellite_dev' : ['frseldev0001.sel.fr.corp',],        # Nagios Dev Satellite
    'mas'           : ['mas-master.app.corp',],             # MAS - Monitoring Automation Server
    'sas'           : ['sas-master.app.corp',],             # SAS - Shinken Arbiter Server
    'omnibus'       : ['hypervision.app.corp',],            # Omnibus related servers
    'satellites'    : get_satellites_list(),                # All Nagios Satellites in production
    'debian'        : [],                                   # All debian based systems
    'redhat'        : [],                                   # All redhat based systems
    'puppet_managed': [],                                   # Hosts managed by puppet
}

# ----------
# CATEGORIES
# ----------
#
# Hosts by operating systems
env.roledefs['debian'].extend(env.roledefs['admin'])
env.roledefs['debian'].extend(env.roledefs['satellites'])
env.roledefs['debian'].extend(env.roledefs['central'])
env.roledefs['debian'].extend(env.roledefs['mas'])
env.roledefs['debian'].extend(env.roledefs['sas'])
env.roledefs['redhat'].extend(env.roledefs['omnibus'])

# Hosts managed by Puppet
env.roledefs['puppet_managed'].extend(env.roledefs['admin'])
env.roledefs['puppet_managed'].extend(env.roledefs['mas'])
env.roledefs['puppet_managed'].extend(env.roledefs['sas'])
env.roledefs['puppet_managed'].extend(env.roledefs['omnibus'])
env.roledefs['puppet_managed'].extend(env.roledefs['central'])

#-------------------------------------------------------------------------------
env.roles.extend(env.roledefs.keys())
