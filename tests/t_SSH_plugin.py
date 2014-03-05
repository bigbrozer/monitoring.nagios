# -*- coding: utf-8 -*-
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

"""Test module for SSH based plugins."""

import unittest
import sys

sys.path.insert(0, "..")
from monitoring.nagios.plugin import NagiosPluginSSH
from monitoring.nagios.probes import ProbeSSH


class TestPluginPubKey(unittest.TestCase):
    """
    Connect using SSH using pub key.
    """

    def setUp(self):
        sys.argv = sys.argv[:1]
        args = [
            '-H', 'monitoring-dc.app.corp',
        ]
        sys.argv.extend(args)
        self.plugin = NagiosPluginSSH()

    def tearDown(self):
        self.plugin.ssh.close()

    def test_ssh_remote_cmd(self):
        """Test execution of a remote command using SSH."""
        command = self.plugin.ssh.execute('ls -ld /boot')
        self.assertIn('/boot', command.output.pop())

    def test_ssh_list_files_in_dir(self):
        """Test listing files in a directory using SSH."""
        files = self.plugin.ssh.list_files('/')
        self.assertIn('/root', files)

    def test_ssh_list_files_with_glob(self):
        """Test listing files matching a pattern using SSH."""
        files = self.plugin.ssh.list_files('/var/log', '*.log')
        self.assertIn('/var/log/kern.log', files)

    def test_ssh_get_file_lastmodified_timestamp(self):
        """Test to get the last modified timestamp of a file using SSH."""
        timestamp = self.plugin.ssh.get_file_lastmodified_timestamp(
            '/var/log/kern.log', stime='~/stime')
        self.assertIsInstance(timestamp, int)

    def test_ssh_missing_stime(self):
        """Test failure when stime binary cannot be found."""
        with self.assertRaises(ProbeSSH.SSHError):
            self.plugin.ssh.get_file_lastmodified_timestamp(
                '/var/log/kern.log')


class TestPluginUserPass(unittest.TestCase):
    """Connect using SSH with user / password."""
    def setUp(self):
        sys.argv = sys.argv[:1]
        args = [
            '-H', 'srv1faurdca.idc.us.corp',
            '-u', 'fcspi',
            '-p', 'fcspi1',
        ]
        sys.argv.extend(args)
        self.plugin = NagiosPluginSSH()

    def tearDown(self):
        self.plugin.ssh.close()

    def test_ssh_remote_command(self):
        """Test SSH remote command execution using a user / password."""
        command = self.plugin.ssh.execute('ls -ld /boot')
        self.assertIn('/boot', command.output.pop())


class TestProbeSSH(unittest.TestCase):
    """Establish a SSH connection on remote host using Probe."""
    def tearDown(self):
        if hasattr(self, 'ssh'):
            self.ssh.close()

    def test_ssh_pubkey_login(self):
        """Test SSH connection using public key."""
        self.ssh = ProbeSSH('monitoring-dc.app.corp')

    def test_ssh_askpass_login(self):
        """Test SSH connection using a username / password."""
        self.ssh = ProbeSSH('srv1faurdca.idc.us.corp',
                            username='fcspi',
                            password='fcspi1')

    def test_ssh_timeout(self):
        """Test failure when connection timeout."""
        with self.assertRaises(SystemExit):
            self.ssh = ProbeSSH('wwfcsunia316.fcs.toa.prim', timeout=1)

    def test_ssh_host_not_found(self):
        """Test failure when host cannot be resolved."""
        with self.assertRaises(SystemExit):
            self.ssh = ProbeSSH('wwfcsunigdsa316.fcs.toa.prim')

    def test_ssh_no_route(self):
        """Test failure when host cannot be reached."""
        with self.assertRaises(SystemExit):
            self.ssh = ProbeSSH('10.56.89.45')

    def test_ssh_command_timeout(self):
        """Test SSH remote command timeout trigger."""
        self.ssh = ProbeSSH('monadm.edc.eu.corp', timeout=1)
        with self.assertRaises(self.ssh.SSHCommandTimeout):
            self.ssh.execute('sleep 5 && echo success')