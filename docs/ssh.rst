=================
SSH based plugin
=================

.. currentmodule:: monitoring.nagios.plugin

The class :class:`NagiosPluginSSH` that inherits from :class:`NagiosPlugin` is
responsible to init a plugin that makes use of SSH to check something.

If you show the help with ``--help``, you will see extra arguments provided by
the class. It uses the same mechanics as we saw in :doc:`new_plugin` section. It
overrides :meth:`NagiosPlugin.define_plugin_arguments` to define new arguments
and :meth:`NagiosPlugin.verify_plugin_arguments` to do arguments checking.

Getting started
===============

Instanciate a new SSH plugin with::

 >>> import logging
 >>> from monitoring.nagios.plugin import NagiosPluginSSH

 >>> logger = logging.getLogger('plugin')

 >>> plugin = NagiosPluginSSH(version="1.0",
 >>>                          description="Do something using SSH.")

Default plugin arguments
========================

The class defines the following default set of arguments.

- ``-H``: The hostaddress of the server to connect on.
- ``-P``: Port to connect to (default to 22).
- ``-u, --username``: Login user. Default to current logged in user.
- ``-p, --password``: Login user password. Default is to use pub key of the
  current user.
- ``-t, --timeout``: Connection timeout in seconds (default to 10 secs).

.. currentmodule:: monitoring.nagios.probes.secureshell

Remote actions
==============

Use attribute ``ssh`` to make use of the SSH probe. Look at deeper details
within the API reference for :class:`ProbeSSH` class.

Get a command output
--------------------

Here is how you can execute a command::

 >>> cmd = plugin.ssh.execute("ls -l /")

This will return a :class:`CommandResult` instance with useful attributes like
:attr:`CommandResult.output` for lines on stdout, :attr:`CommandResult.errors`
for lines on stderr and :attr:`CommandResult.status` for status code of the
command.

Read output of the command and get a list with::

 >>> cmd.output
 ['total 160',
 'drwxr-xr-x   2 root root  4096 janv. 15 08:53 bin',
 'drwxr-xr-x   4 root root 12288 f\xc3\xa9vr. 25 17:41 boot',
 'drwxr-xr-x   2 root root  4096 d\xc3\xa9c.   4  2012 cdrom',
 'drwxr-xr-x  16 root root  4280 mars   5 08:38 dev',
 'drwxr-xr-x 170 root root 12288 mars   5 08:38 etc',
 'drwxr-xr-x   3 root root  4096 d\xc3\xa9c.   4  2012 home',
 '...']

As this is a list, you can easily iterate over each lines::

 >>> for line in cmd.output:
 >>>     # Do something with line...

The method :meth:`ProbeSSH.execute` will raise
:class:`ProbeSSH.SSHCommandTimeout` exception if timeout is reached (as
defined by the ``-t`` plugin argument).

You can also get the command status code instead::

 >>> if cmd.status == 0:
 >>>    print "Command executed successfully ;-)"

Get a list of files in a directory
----------------------------------

The SSH probe has suppport to easily find files within a directory that match a
pattern. It has support for recursion but disabled by default.

Search for ``*.txt`` files in ``/tmp``::

 >>> text_files = plugin.ssh.list_files(directory="/tmp", glob="*.txt")
 ['/tmp/c.txt',
 '/tmp/e.txt',
 '/tmp/d.txt',
 '/tmp/o.txt',
 '/tmp/t.txt',
 '/tmp/y.txt',
 '/tmp/b.txt',
 '/tmp/r.txt',
 '/tmp/a.txt']

Now with recursion up to 5 sub-directories::

 >>> text_files = plugin.ssh.list_files(directory="/tmp", glob="*.txt", depth=5)
 ['/tmp/c.txt',
 '/tmp/e.txt',
 '/tmp/d.txt',
 '/tmp/o.txt',
 '/tmp/tata/a.txt',
 '/tmp/t.txt',
 '/tmp/y.txt',
 '/tmp/toto/b/b.txt',
 '/tmp/toto/c/b.txt',
 '/tmp/toto/a/b.txt',
 '/tmp/b.txt',
 '/tmp/r.txt',
 '/tmp/a.txt']

Get file or directory last modified time
----------------------------------------

The SSH probe defines methods to obtain the last modified time of a file or
directory.

:meth:`ProbeSSH.get_file_lastmodified_minutes` will give you for how much
minutes the file was last modified.

:meth:`ProbeSSH.get_file_lastmodified_timestamp` will give you the last modified
time as a Unix Timestamp (UTC).

Example::

 >>> plugin.ssh.get_file_lastmodified_minutes("/etc/motd")
 16
 >>> plugin.ssh.get_file_lastmodified_timestamp("/etc/motd")
 1294765528
