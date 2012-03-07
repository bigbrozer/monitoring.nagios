# -*- coding: UTF-8 -*-
#===============================================================================
# Filename      : packages
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : APT module to manage debian packages (upgrade, install...).
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

from fabric.api import task, sudo, puts, roles
from fabric.colors import yellow

@task
@roles('debian')
def autoremove():
    """Auto remove unnecessary packages."""
    sudo('apt-get autoremove')

@task
@roles('debian')
def update():
    """Update the package list."""
    puts(yellow('\t- Updating package list...'))
    sudo('apt-get -qq update')

@task
@roles('debian')
def full_upgrade(interactive='yes'):
    """
    Do a full system packages update on all systems.

    USAGE
    -----

      $ fab nagios.full_upgrade[:OPTIONS][,OPTIONS...]

    OPTIONS
    -------

      interactive=(yes)|no       Does upgrade should be interactive ?

    """
    apt_options = 'Vq'

    if interactive == 'no':
        apt_options = 'Vqy'

    puts(yellow('Applying system update...', bold=True))
    update()
    sudo('apt-get -%s dist-upgrade' % apt_options)
    autoremove()
