# -*- coding: UTF-8 -*-
#===============================================================================
# Filename      : tasks
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : Nagios module to be used by fabric.
#                 Contains functions to execute tasks on Nagios satellites.
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

from fabric.api import env, roles, parallel, settings, hide, get, task, sudo, cd, put, puts
from fabric.colors import blue, yellow, green, red
from monitoring.fabric.nagios.log import Log

#-------------------------------------------------------------------------------
# Task: nagios.deploy
#-------------------------------------------------------------------------------
@task
@roles('satellites')
@parallel
def deploy(no_service=False):
    """
    Deploy Nagios configuration on all satellites.

    USAGE
    -----

      $ fab nagios.deploy[:OPTIONS][,OPTIONS...]

    OPTIONS
    -------

      no_service=<True|False>       If set to True, show warning for hosts that
                                    have no service defined. (Default: False)
    """

    env.linewise = True

    with settings(hide('warnings', 'stdout', 'running'), warn_only=True):
        print blue('===> Starting deploying new Nagios configuration on %s...' % yellow(env.host, bold=True), bold=True)
        nagios_config_result = sudo('/usr/local/nagios/admin/update-nagios-config.sh', user='nagios')
        get('/usr/local/nagios/var/last_export.log', 'log/nagdeploy_%(host)s.log')
        log = Log(env.host)

        # Check results
        if nagios_config_result.failed:
            puts(red(\
'''
 _   _       _         _ _              _ _ 
| \ | | __ _| |__   __| (_)_ __   ___  | | |
|  \| |/ _` | '_ \ / _` | | '_ \ / _ \ | | |
| |\  | (_| | | | | (_| | | | | |  __/ |_|_|
|_| \_|\__,_|_| |_|\__,_|_|_| |_|\___| (_|_)

''', bold=True))
            puts(red("\nErrors must be corrected:\n=========================\n\n%s\n" % log.errors))
        else:
            if log.duplicates:
                puts(red("\nDuplicates exist:\n=================\n\n%s\n" % log.duplicates))
            if log.host_has_no_service and no_service:
                puts(yellow("\nHosts that have no service defined:\n===================================\n\n%s\n" % log.host_has_no_service))

#-------------------------------------------------------------------------------
# Task: nagios.setup
#-------------------------------------------------------------------------------
@task
@roles('satellites')
def setup():
    """Deploy Nagios system image changes on all satellites."""
    print blue('==== Deploying new Nagios system image on %s ====' % yellow(env.host, bold=True), bold=True)
    sudo('rm -rf /tmp/sat_update')
    sudo('svn export --depth files "http://monitoring-dc.app.corp/svn/nagios_dc_system_image/trunk" "/tmp/sat_update"')
    with cd('/tmp/sat_update'):
        sudo('make init')


#-------------------------------------------------------------------------------
# Task: nagios.clean_old_graphs
#-------------------------------------------------------------------------------
@task
@roles('satellites')
def clean_old_graphs():
    """Clean the old graphs of removed hosts from satellites."""
    sudo('find /usr/local/pnp4nagios/var/perfdata -mindepth 1 -type d -ctime +15 -exec rm -rfv {} +' ,user='nagios')

#-------------------------------------------------------------------------------
# Task: nagios.list_graphs
#-------------------------------------------------------------------------------
@task
@roles('satellites')
def list_graphs():
    """Show a list of all hosts that have graphs. (debug)"""
    sudo('find /usr/local/pnp4nagios/var/perfdata -mindepth 1 -type d -exec ls -1drt {} +' ,user='nagios')

#-------------------------------------------------------------------------------
# Task: nagios.update_cssh
#-------------------------------------------------------------------------------
@task
@roles('admin')
def update_cssh():
    """Update Cluster SSH list of satellites on the Administration Server."""
    header = """\
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# THIS FILE IS MANAGED BY MONITORING TOOLS
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
# If you edit this file manually, damn god ! you risk to loose what have been
# done here ! Advice is to use Monitoring Tools.
#
"""
    nagprod = 'nagprod\t\t%s\n' % ' '.join(env.roledefs['satellites'])
    nagdev = 'nagdev\t\t%s %s\n' % ( ' '.join(env.roledefs['satellite_dev']), ' '.join(env.roledefs['satellite_tpl']) )

    conf = [header, nagprod, nagdev]

    with open('tmp/clusters', 'w') as clusters_file:
        clusters_file.writelines(conf)

    put('tmp/clusters', '/etc/clusters', use_sudo=True, mode=0644)
