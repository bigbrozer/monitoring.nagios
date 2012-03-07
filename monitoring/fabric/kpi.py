# -*- coding: UTF-8 -*-
#===============================================================================
# Filename      : kpi
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : KPI & Passwords management tasks.
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

from os.path import expanduser, exists
from fabric.api import env, task, hosts, local, puts, settings, hide
from fabric.colors import red

@task
@hosts('localhost')
def passdb():
    """
    Open the password database for Monitoring & Reporting.
    """
    # Ask user credentials
    if not exists(expanduser('~/.gvfs/sel sur frselfls0003.sel.fr.corp')):
        d = raw_input('Enter Windows domain [FR-CORP]: ')
        u = raw_input('Enter Windows username: ')
        puts(red('You will be asked to enter your Windows user password !', bold=True))

        # Defaults values
        if not d:
            d = 'FR-CORP'

        credentials = '%s;%s@' % (d, u)

        # Mount share
        passdb_mount_command = "gvfs-mount \'smb://%sfrselfls0003.sel.fr.corp/SEL\'" % credentials
        with settings(hide('running')):
            local(passdb_mount_command)
    
    # Launch keepass
    puts('Database share is already mounted, skip mount.')
    with settings(hide('running')):
        local("keepassx \'%s/.gvfs/sel sur frselfls0003.sel.fr.corp/IT-Ope/OPERATIONS/ITOP-Monitoring/Database/Passwords.kdb\'" % expanduser('~'))
