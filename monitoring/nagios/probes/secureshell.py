# -*- coding: utf-8 -*-
#===============================================================================
# Filename      : secureshell
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

import os
from datetime import datetime
import logging as log
import string

from monitoring.nagios.probes import Probe
from monitoring.nagios.plugin.exceptions import NagiosUnknown
import ssh

logger = log.getLogger('monitoring.nagios.probes')


class CommandResult(object):
    """
    This class is for manipulating a remote command execution result.

    It takes a :class:`ssh.Channel` object as his first parameter. Then provides
    the following attributes:

    .. attribute:: CommandResult.input

        This is stdin for the command.

    .. attribute:: CommandResult.output

        This is stdout or output of the command.

    .. attribute:: CommandResult.errors

        This is stderr or all errors for the command.

    .. attribute:: CommandResult.status

        The command exit code.
    """
    def __init__(self, channel):
        self.input = channel.makefile('wb', -1)
        self.output = channel.makefile('rb', -1).readlines()
        self.errors = channel.makefile_stderr('rb', -1).readlines()
        self.status = channel.recv_exit_status()


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
    :param timeout: Connection timeout in seconds (default to 10 secs).
    :type timeout: float
    """
    class SSHError(Exception):
        pass


    class SSHCommandFailed(SSHError):
        pass


    def __init__(self, hostaddress='', port=22, username=None, password=None, timeout=10.0):
        super(ProbeSSH, self).__init__(hostaddress, port)

        self.timeout = timeout

        try:
            self._ssh_client = ssh.SSHClient()
            self._ssh_client.set_missing_host_key_policy(ssh.MissingHostKeyPolicy())
            self._ssh_client.connect(hostaddress, port, username, password, timeout=self.timeout, compress=True)
        except ssh.SSHException as e:
            raise NagiosUnknown('''Cannot establish a SSH connection on remote server !
Host: %s
Port: %s
Message: %s''' % (self._hostaddress, self._port, e))
        except Exception as e:
            raise NagiosUnknown('''Unexpected error during SSH connection !
Host: %s
Port: %s
Message: %s''' % (self._hostaddress, self._port, e))

    def execute(self, command, timeout=None):
        """
        Execute a command on the remote server and return results.

        :param command: Command line to execute on the remote server.
        :type command: str, unicode
        :param timeout: Command execution timeout. Default to 10 secs.
        :type timeout: float
        :return: An instance of :class:`CommandResult`.
        """
        logger.debug('Execute SSH command: {}'.format(command))

        # Set global timeout if not specified
        if not timeout: timeout = self.timeout
        logger.debug('Timeout is set to %f.', timeout)

        chan = self._ssh_client.get_transport().open_session()
        chan.settimeout(timeout)
        chan.exec_command(command)
        cmd_results = CommandResult(chan)

        return cmd_results

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
        stdout = self.execute(find).output
        files = map(string.strip, stdout)
        return files

    def get_file_lastmodified_timestamp(self, filename, stime='/usr/local/nagios/bin/stime'):
        """
        Return the last modified Unix Epoch timestamp of a file.

        :param filename: path to the file that should be checked.
        :param stime: location of the stime binary. Default to ``/usr/local/nagios/bin/stime``.
        :return: Unix timestamp.
        :rtype: int
        """
        logger.debug('Calling method get_file_lastmodified_timestamp().')

        if not os.path.exists(stime):
            raise self.SSHCommandFailed('Unable to locate stime command !\nPath: {}'.format(stime))

        stime = "{0} -m {1}".format(stime, filename)
        command = self.execute(stime)
        if command.status:
            raise self.SSHCommandFailed('Problem during the execution of stime !\nCommand: {}'.format(stime))

        ts = command.output.pop()
        try:
            ts = int(ts)
        except ValueError as e:
            raise self.SSHError("Unexpected result in output of stime: {}".format(e))

        return ts

    def get_file_lastmodified_minutes(self, filename, **kwargs):
        """
        Return minutes since file was last modified.

        :param filename: path to the file that should be checked.
        :return: Minutes.
        :rtype: int
        """
        logger.debug('Calling method get_file_lastmodified_minutes().')

        last_modified_timestamp = self.get_file_lastmodified_timestamp(filename, **kwargs)
        now = datetime.today()
        last_modified_totalsecs = (now - datetime.fromtimestamp(last_modified_timestamp)).total_seconds()
        last_modified_time = divmod(last_modified_totalsecs, 60)
        return int(last_modified_time[0])
