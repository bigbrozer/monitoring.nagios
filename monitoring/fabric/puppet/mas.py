# -*- coding: UTF-8 -*-
#===============================================================================
# Filename      : mas
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : MAS Server Administration tasks.
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

from fabric.api import env, task, roles, hosts, run, cd, puts, settings

@task
@hosts('mas-master.app.corp')
def update():
    """
    Update to the latest configuration on Puppet Master.
    """
    env.user = 'root'
    with cd('/etc/puppet'):
        run('git pull')

@task
@roles('puppet_managed')
def apply(test='yes'):
    """
    Apply configuration from Puppet Master to all Puppet Agents
    """
    env.user = 'root'

    with settings(warn_only=True):
        if test == 'yes':
            run('puppet agent --test --noop')
        else:
            run('puppet agent --test')

@task
@roles('puppet_managed')
def disable_agent():
    """
    Disable all Puppet agents on servers managed by it.
    """
    env.user = 'root'
    run('puppet agent --disable')

@task
@roles('puppet_managed')
def enable_agent():
    """
    Enable all Puppet agents on servers managed by it.
    """
    env.user = 'root'
    run('puppet agent --enable')
