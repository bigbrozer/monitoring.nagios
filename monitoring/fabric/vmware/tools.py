# -*- coding: UTF-8 -*-
#===============================================================================
# Filename      : tools
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : Tasks to manage Vmware Tools on our servers.
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

from fabric.api import env, task, hosts, roles, run, cd, put

vmware_tools_archive = "data/vmware_tools/vmware_tools-8.3.12-493255.tar.gz"

@task
@hosts('')
def install():
    """
    Install VMware tools on remote server.
    """
    env.user = 'root'

    put(vmware_tools_archive, '/tmp/vmware_tools.tar.gz')
    with cd('/tmp'):
        run('tar zxf vmware_tools.tar.gz')
        with cd('vmware-tools-distrib'):
            run('./vmware-install.pl')

