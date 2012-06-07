# -*- coding: UTF-8 -*-
#===============================================================================
# Module        : fabfile
# Author        : Vincent BESANCON aka 'v!nZ' <besancon.vincent@gmail.com>
# Description   : Fabric tasks to manage the project.
#-------------------------------------------------------------------------------
# This file is part of NagiosPPT (Nagios Python Plugin Template).
#
# NagiosPPT is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NagiosPPT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NagiosPPT.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

"""
Fabric tasks for project monitoring.nagios.
"""

from fabric.api import task, sudo, roles
from monitoring.fabric import servers

#-------------------------------------------------------------------------------
@task
@roles('satellites', 'satellite_dev', 'satellite_tpl')
def install():
    """Install / upgrade package on all Nagios satellites."""
    sudo('http_proxy=\"http://monitoring-dc.app.corp:8080/\" pip install git+http://monitoring-dc.app.corp/git/lib/monitoring.nagios.git')

#-------------------------------------------------------------------------------
@task
@roles('satellites', 'satellite_dev', 'satellite_tpl')
def uninstall():
    """Uninstall package on all Nagios satellites."""
    sudo('pip uninstall -y monitoring.nagios')

