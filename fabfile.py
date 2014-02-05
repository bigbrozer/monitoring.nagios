# -*- coding: UTF-8 -*-
# Copyright (C) Vincent BESANCON <besancon.vincent@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
Fabric tasks for project monitoring.nagios.
"""

import os

from fabric.api import (
    env,
    task,
    hosts,
    local,
)
from fabric.contrib.project import rsync_project
from monitoring.fabric import servers


@task
@hosts('monitoring-dc.app.corp')
def doc():
    """Upload doc to central server"""
    env.user = "webcontent"

    DOCROOT = '/var/www/project'
    DOCDIR = os.path.join(DOCROOT, 'monitoring.nagios')

    local('make doc')
    rsync_project(DOCDIR, 'docs/_build/html/', delete=True)
