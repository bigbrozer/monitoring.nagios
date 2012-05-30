# -*- coding: utf-8 -*-
#===============================================================================
# Filename      : t_SSH_plugin
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : Test SSH plugin creation.
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

import unittest
import sys

from monitoring.nagios.plugin import NagiosPluginSSH
from monitoring.nagios.plugin.probes import ProbeSSH

class TestPluginPubKey(unittest.TestCase):
    """
    Connect using SSH using pub key.
    """

    def setUp(self):
        sys.argv[1] = '-H'
        sys.argv[2] = 'monitoring-dc.app.corp'
        self.plugin = NagiosPluginSSH()

    def tearDown(self):
        self.plugin.ssh.close()

    def test_ssh_remote_cmd(self):
        stdout, stderr = self.plugin.ssh.execute('ls -ld /boot')
        self.assertIn('/boot', stdout.readline())

    def test_ssh_list_files_in_dir(self):
        files = self.plugin.ssh.list_files('/')
        self.assertIn('/root', files)

    def test_ssh_list_files_with_glob(self):
        files = self.plugin.ssh.list_files('/var/log', '*.log')
        self.assertIn('/var/log/kern.log', files)


class TestPluginUserPass(unittest.TestCase):
    """
    Connect using SSH with user / password.
    """

    def setUp(self):
        args = [
            '-H', 'srv1faurdca.idc.us.corp',
            '-u', 'fcspi',
            '-p', 'fcspi1',
        ]
        sys.argv.extend(args)
        self.plugin = NagiosPluginSSH()

    def tearDown(self):
        self.plugin.ssh.close()

    def test_ssh_user_password(self):
        stdout, stderr = self.plugin.ssh.execute('ls -ld /boot')
        self.assertIn('/boot', stdout.readline())


class TestProbeSSH(unittest.TestCase):
    """
    Establish a SSH connection on remote host using Probe.
    """

    def tearDown(self):
        self.ssh.close()

    def test_ssh_pubkey_login(self):
        self.ssh = ProbeSSH('monitoring-dc.app.corp')

    def test_ssh_askpass_login(self):
        self.ssh = ProbeSSH('srv1faurdca.idc.us.corp', username='fcspi', password='fcspi1')
