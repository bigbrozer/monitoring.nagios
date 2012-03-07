# -*- coding: UTF-8 -*-
#===============================================================================
# Filename      : central
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : Central Server module to do tasks on it.
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

from fabric.api import env, task, roles, run, cd, puts

@task
@roles('central')
def thruk_update():
    """
    Update Thruk on remote central server.
    
    Do this after a push to the Thruk repository to apply the update and restart
    the FastCGI process.
    """
    env.user = 'dashboard'
    puts('Connecting as user \'%(user)s\'.' % env)
    with cd('Thruk'):
        run('git pull')
        run('perl Makefile.PL')
        run('make')
        run('/etc/init.d/thruk_fastcgi_server.sh restart')

@task
@roles('central')
def optools_update():
    """
    Update IT Operations Tools on remote central server.
    
    Do this after a push to the optools repository to apply the update
    """
    env.user = 'django'
    puts('Connecting as user \'%(user)s\'.' % env)
    with cd('optools'):
        run('git pull')
        run('./manage.py collectstatic')
