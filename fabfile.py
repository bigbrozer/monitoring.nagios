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

from fabric.api import task, sudo, roles
from monitoring.fabric import servers

@task
@roles('satellites', 'satellite_dev', 'satellite_tpl')
def upgrade():
    """Upgrade Monitoring package."""
    sudo('pip install git+http://monitoring-dc.app.corp/git/lib/monitoring.git --upgrade')
