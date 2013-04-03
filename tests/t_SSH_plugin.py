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
from monitoring.nagios.probes import ProbeSSH

class TestPluginPubKey(unittest.TestCase):
    """
    Connect using SSH using pub key.
    """

    def setUp(self):
        sys.argv= sys.argv[:1]
        args = [
            '-H', 'monitoring-dc.app.corp',
        ]
        sys.argv.extend(args)
        self.plugin = NagiosPluginSSH()

    def tearDown(self):
        self.plugin.ssh.close()

    def test_ssh_remote_cmd(self):
        command = self.plugin.ssh.execute('ls -ld /boot')
        self.assertIn('/boot', command.output.pop())

    def test_ssh_list_files_in_dir(self):
        files = self.plugin.ssh.list_files('/')
        self.assertIn('/root', files)

    def test_ssh_list_files_with_glob(self):
        files = self.plugin.ssh.list_files('/var/log', '*.log')
        self.assertIn('/var/log/kern.log', files)

    def test_ssh_get_file_lastmodified_timestamp(self):
        timestamp = self.plugin.ssh.get_file_lastmodified_timestamp('/var/log/kern.log', stime='~/stime')
        self.assertIsInstance(timestamp, int)

    def test_ssh_missing_stime(self):
        with self.assertRaises(ProbeSSH.SSHError):
            timestamp = self.plugin.ssh.get_file_lastmodified_timestamp('/var/log/kern.log')


class TestPluginUserPass(unittest.TestCase):
    """
    Connect using SSH with user / password.
    """

    def setUp(self):
        sys.argv= sys.argv[:1]
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
        command = self.plugin.ssh.execute('ls -ld /boot')
        self.assertIn('/boot', command.output.pop())


class TestProbeSSH(unittest.TestCase):
    """
    Establish a SSH connection on remote host using Probe.
    """

    def tearDown(self):
        if hasattr(self, 'ssh'): self.ssh.close()

    def test_ssh_pubkey_login(self):
        self.ssh = ProbeSSH('monitoring-dc.app.corp')

    def test_ssh_askpass_login(self):
        self.ssh = ProbeSSH('srv1faurdca.idc.us.corp', username='fcspi', password='fcspi1')

    def test_ssh_timeout(self):
        with self.assertRaises(SystemExit):
            self.ssh = ProbeSSH('wwfcsunia316.fcs.toa.prim', timeout=1)

    def test_ssh_host_not_found(self):
        with self.assertRaises(SystemExit):
            self.ssh = ProbeSSH('wwfcsunigdsa316.fcs.toa.prim')

    def test_ssh_no_route(self):
        with self.assertRaises(SystemExit):
            self.ssh = ProbeSSH('10.56.89.45')
