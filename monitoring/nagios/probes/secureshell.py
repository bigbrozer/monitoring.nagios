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

"""SSH probe module."""

import logging as log
import string
import socket
from datetime import datetime

import ssh

from monitoring.nagios.probes import Probe
from monitoring.nagios.exceptions import NagiosUnknown


logger = log.getLogger('monitoring.nagios.probes')


class CommandResult(object):
    """
    This class is for manipulating a remote command execution result.

    It takes a :class:`ssh.Channel` object as his first parameter. Then
    provides the following attributes:

    .. attribute:: CommandResult.input

        This is stdin for the command.

    .. attribute:: CommandResult.output

        This is a list of lines on stdout or output of the command.

    .. attribute:: CommandResult.errors

        This is a list of lines on stderr or all errors for the command.

    .. attribute:: CommandResult.status

        An integer for the command exit code.
    """
    def __init__(self, channel):
        self.input = channel.makefile('wb', -1)
        self.output = map(string.strip, channel.makefile('rb', -1).readlines())
        self.errors = map(
            string.strip, channel.makefile_stderr('rb', -1).readlines())
        self.status = channel.recv_exit_status()


class ProbeSSH(Probe):
    """
    A SSH probe.

    :param hostaddress: The host to connect to.
    :type hostaddress: str
    :param port: The remote port the remote host listen on.
    :type port: int
    :param username: Login user name. Default is to use the current
                     authenticated user.
    :type username: str
    :param password: Login user password. Default is to use the public key.
    :type password: str
    :param timeout: Connection timeout in seconds (default to 10 secs).
    :type timeout: float
    """
    class SSHError(Exception):
        """Base class for all SSH related errors."""
        def __init__(self, message):
            self.message = message

        def __str__(self):
            return self.message

    class SSHCommandFailed(SSHError):
        """Exception triggered when a SSH command has failed."""
        pass

    class SSHCommandNotFound(SSHError):
        """Exception triggered when a SSH command is not found."""
        pass

    class SSHCommandTimeout(SSHError):
        """Exception triggered when a SSH command timed out."""
        pass

    def __init__(self, hostaddress='', port=22, username=None, password=None,
                 timeout=10.0):
        super(ProbeSSH, self).__init__()

        self.hostaddress = hostaddress
        self.username = username
        self._password = password
        self.port = port
        self.timeout = timeout

        try:
            self._ssh_client = ssh.SSHClient()
            self._ssh_client.set_missing_host_key_policy(
                ssh.MissingHostKeyPolicy())
            self._ssh_client.connect(self.hostaddress,
                                     self.port,
                                     self.username,
                                     self._password,
                                     timeout=self.timeout,
                                     compress=True)
        except ssh.SSHException as e:
            raise NagiosUnknown('''Cannot establish a SSH connection on remote
server !
Host: %s
Port: %s
Message: %s''' % (self.hostaddress, self.port, e))
        except Exception as e:
            raise NagiosUnknown('''Unexpected error during SSH connection !
Host: %s
Port: %s
Message: %s''' % (self.hostaddress, self.port, e))

    def execute(self, command, timeout=None):
        """
        Execute a command on the remote server and return results.

        :param command: Command line to execute on the remote server.
        :type command: str, unicode
        :param timeout: Command execution timeout. Default to 10 secs.
        :type timeout: float
        :return: An instance of :class:`CommandResult`.

        :raises ProbeSSH.SSHCommandTimeout: if executed command timed out.
        """
        logger.debug('Execute SSH command: {}'.format(command))

        # Set global timeout if not specified
        if not timeout:
            timeout = self.timeout
        logger.debug('Timeout is set to %f.', timeout)

        try:
            chan = self._ssh_client.get_transport().open_session()
            chan.settimeout(timeout)
            chan.exec_command(command)
            cmd_results = CommandResult(chan)
        except socket.timeout:
            raise self.SSHCommandTimeout("The command execution has timed out !"
                                         "\nCommand: {}"
                                         "\nTimeout: {}s".format(command,
                                                                timeout))

        return cmd_results

    def close(self):
        """
        Close the SSH connection.
        """

        self._ssh_client.close()

    def list_files(self, directory='.', glob='*', depth=1):
        """
        List all files in a directory. Optionnaly, you can specify a regexp to
        filter files.

        :param directory: Directory to look in. Default is the current working
                          directory.
        :type directory: str
        :param glob: Pattern to filter files. Default to '*' all.
        :type glob: str
        :param depth: Recursive level for scanning files. Default to disable
                      recursive scanning.
        :type depth: int
        :return: list(str)
        """

        find = 'find {0} -name \'{1}\' -maxdepth {2}'.format(
            directory, glob, depth)
        files = self.execute(find).output
        return files

    def get_file_lastmodified_timestamp(self, filename,
                                        stime='/usr/local/nagios/bin/stime'):
        """
        Return the last modified Unix Epoch timestamp of a file.

        :param filename: path to the file that should be checked.
        :param stime: location of the stime binary. Default to
                      ``/usr/local/nagios/bin/stime``.
        :return: Unix timestamp.
        :rtype: int
        """
        logger.debug('Calling method get_file_lastmodified_timestamp().')

        stime_command = "{0} -m {1}".format(stime, filename)
        command = self.execute(stime_command)
        if command.status == 127:
            raise self.SSHCommandNotFound(
                'Unable to find stime binary: {} !'.format(stime))
        elif command.status != 0:
            raise self.SSHCommandFailed(
                'Problem during the execution of stime !\n'
                'Command: {0}\n'
                'Output: {1.output}\n'
                'Errors: {1.errors}'.format(stime_command, command))

        ts = command.output.pop()
        try:
            ts = int(ts)
        except ValueError as e:
            raise self.SSHError(
                "Unexpected result in output of stime: {}".format(e))

        return ts

    def get_file_lastmodified_minutes(self, filename, **kwargs):
        """
        Return minutes since file was last modified.

        :param filename: path to the file that should be checked.
        :return: Minutes.
        :rtype: int
        """
        logger.debug('Calling method get_file_lastmodified_minutes().')

        last_modified_timestamp = self.get_file_lastmodified_timestamp(
            filename, **kwargs)
        now = datetime.today()
        last_modified_totalsecs = (now - datetime.fromtimestamp(
            last_modified_timestamp)).total_seconds()
        last_modified_time = divmod(last_modified_totalsecs, 60)
        return int(last_modified_time[0])
