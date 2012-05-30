# -*- coding: utf-8 -*-
#===============================================================================
# Filename      : monitoring.nagios.plugin.probes.secureshell
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : Module that define a SSH probe.
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

import logging as log
import string

from monitoring.nagios.plugin.probes import Probe
from monitoring.nagios.plugin.exceptions import NagiosUnknown
import ssh

logger = log.getLogger('monitoring.nagios.plugin.probes')


class ProbeSSH(Probe):
    """
    A SSH probe.

    :param hostaddress: The host to connect to.
    :type hostaddress: str
    :param port: The remote port the remote host listen on.
    :type port: int
    :param username: Login user name. Default is to use the current authenticated user.
    :type username: str
    :param password: Login user password. Default is to use the public key.
    :type password: str
    """

    def __init__(self, hostaddress='', port=22, username=None, password=None):
        super(ProbeSSH, self).__init__(hostaddress, port)

        try:
            self._ssh_client = ssh.SSHClient()
            self._ssh_client.load_system_host_keys()
            self._ssh_client.set_missing_host_key_policy(ssh.AutoAddPolicy())
            self._ssh_client.connect(hostaddress, port, username, password, compress=True)
        except ssh.SSHException as e:
            raise NagiosUnknown('''Cannot establish a SSH connection on remote server !
Host: %s
Port: %s
Message: %s''' % (self._hostaddress, self._port, e))

    def execute(self, cmd):
        """
        Execute a command on the remote server and return results.

        :param cmd: Command line to execute on the remote server.
        :type cmd: str
        :return: Tuple of the form (stdout, stderr) each values are file objects.
        """

        stdin, stdout, stderr = self._ssh_client.exec_command(cmd)
        return (stdout, stderr)

    def close(self):
        """
        Close the SSH connection.
        """

        self._ssh_client.close()

    def list_files(self, directory='.', glob='*', depth=1):
        """
        List all files in a directory. Optionnaly, you can specify a regexp to filter files.

        :param directory: Directory to look in. Default is the current working directory.
        :type directory: str
        :param glob: Pattern to filter files. Default to '*' all.
        :type glob: str
        :param depth: Recursive level for scanning files. Default to disable recursive scanning.
        :type depth: int
        :return: list(str)
        """

        find = 'find {0} -name \'{1}\' -maxdepth {2}'.format(directory, glob, depth)
        stdout = self.execute(find)[0]
        files = map(string.strip, stdout.readlines())
        return files
