=================================
Creating a new plugin, the basics
=================================

.. module:: monitoring.nagios.plugin

Introduction
============

The module :mod:`monitoring.nagios.plugin` allows you to create a new plugin
that depends on the type of check it will execute.

This can be a plugin that make use of SNMP, or SSH, or it needs to access a
database and do some query...

There're a class per protocols. I will describe them here.

Basic intialization
===================

The class :class:`NagiosPlugin` is the base class from which all others plugin
classes will inherit. She is reponsible for the plugin initialization and
provides attributes and methods in order to manage plugin output (including
performance data), data rentention saving / loading and plugin arguments.

Initialize a basic plugin, create a file ``my_super_plugin.py``::

 from monitoring.nagios.plugin import NagiosPlugin

 plugin = NagiosPlugin(version='1.0', description='Just a test...')

Try to see the help passing the ``--help`` argument to your plugin::

 usage: my_super_plugin.py [-h] [--debug] [--version] -H HOSTNAME

 Just a test...

 optional arguments:
   -h, --help   show this help message and exit
   --debug      Show debug information, Nagios may truncate output
   --version    show program's version number and exit

 Plugin arguments:
   This arguments are required by the plugin.

   -H HOSTNAME  Target hostname (FQDN or IP address)

Already a bunch of work is done for you ;-)

As you can see, the ``-H`` argument is mandatory.

Logging
-------

Logging is important and you should not neglect it. On first import of
:mod:`monitoring.nagios`, the logging system will be initialized for you. It is
configured to be shown if argument ``--debug`` is passed to your script
(plugin). For the moment it shows only **debug** logging level.

Here is how to use it (based on previous example)::

 import logging
 from monitoring.nagios.plugin import NagiosPlugin

 logger = logging.getLogger('plugin')

 myvar = "Hey !"

 plugin = NagiosPlugin(version='1.0', description='Just a test with logging...')
 logger.debug('Show this message in debug mode only...')
 logger.debug('Content of variable \"myvar\": {0}'.format(myvar))
 logger.debug('This is the end !')

It is mandatory to get the logger named *plugin* with :meth:`logging.getLogger`,
this logger will be used to print debug information related to your plugin.

Now try to start this script with arguments ``-H fake_host --debug`` (``-H`` is
mandatory but will not be verified here), you should notice that the package and
its modules will show a lot of information::

 [DEBUG] (base) === BEGIN PLUGIN INIT ===
 [DEBUG] (base) Debug mode is ON.
 [DEBUG] (base) Plugin class: NagiosPlugin.
 [DEBUG] (base) 	Name: my_super_plugin.py, v1.0
 [DEBUG] (base) 	Desc: Just a test with logging...
 [DEBUG] (base) Processed command line arguments:
 [DEBUG] (base) {   'debug': True, 'hostname': 'fake_host'}
 [DEBUG] (base) Calling second level of initialization.
 [DEBUG] (base) === END PLUGIN INIT ===
 [DEBUG] (my_super_plugin) Show this message in debug mode only...
 [DEBUG] (my_super_plugin) Content of variable "myvar": Hey !
 [DEBUG] (my_super_plugin) This is the end !

The format is ``[LEVEL] (source) message``.

Defining new arguments
----------------------

You need to create a class that inherit from :class:`NagiosPlugin` in order to
add extra arguments to your plugin::

 import logging
 from monitoring.nagios.plugin import NagiosPlugin

 logger = logging.getLogger('plugin')

 class MySuperPlugin(NagiosPlugin):
    pass

 myvar = "Hey !"

 plugin = MySuperPlugin(version='1.0', description='Just a test with logging...')
 logger.debug('Show this message in debug mode only...')
 logger.debug('Content of variable \"myvar\": {0}'.format(myvar))
 logger.debug('This is the end !')

By doing this, you inherit from the base class and by doing this you will be
able to customize as you want some parts of your plugin.

First thing you will want to do is to add new arguments such as thresholds or
whatever. You can add arguments by overriding :meth:`define_plugin_arguments`::

 import logging
 from monitoring.nagios.plugin import NagiosPlugin

 logger = logging.getLogger('plugin')

 class MySuperPlugin(NagiosPlugin):
    def define_plugin_arguments(self):
        super(MySuperPlugin, self).define_plugin_arguments()

 myvar = "Hey !"

 plugin = MySuperPlugin(version='1.0', description='Just a test with logging...')
 logger.debug('Show this message in debug mode only...')
 logger.debug('Content of variable \"myvar\": {0}'.format(myvar))
 logger.debug('This is the end !')

This is called *overriding* because you will change the behavior of the method
:meth:`NagiosPlugin.define_plugin_arguments` but you first call the one in the
super class (the one we inherit from) called :class:`NagiosPlugin` with the help
of :func:`super`. If you forget to call :func:`super`, you will loose arguments
defined in the base class :class:`NagiosPlugin` such as ``-H``, ``--debug``, ...

Let's add a new argument now::

 import logging
 from monitoring.nagios.plugin import NagiosPlugin

 logger = logging.getLogger('plugin')

 class MySuperPlugin(NagiosPlugin):
    def define_plugin_arguments(self):
        super(MySuperPlugin, self).define_plugin_arguments()

        self.required_args.add_argument('-a', '--argument',
                                        dest="argument",
                                        help="This is our new argument.",
                                        required=True)

 myvar = "Hey !"

 plugin = MySuperPlugin(version='1.0', description='Just a test with logging...')
 logger.debug('Show this message in debug mode only...')
 logger.debug('Content of variable \"myvar\": {0}'.format(myvar))
 logger.debug('This is the end !')

:attr:`required_args` is an attribute inherited from :class:`NagiosPlugin`. It
is the default *namespace* or *argument group* for the plugin. You should add
argument to this group only if they are required. Adding argument is done with
:meth:`add_argument` method of :attr:`required_args`, please I strongly advice
you to check out the :mod:`argparse` module documentation which is part of
Python Standard Library.

:meth:`add_argument` has a **required** keyword argument that specify if a error
should be returned if it is required or not (True / False).

Here is the :meth:`add_argument` method in details:

.. py:method:: NagiosPlugin.required_args.add_argument(short_name, [long_name,] dest, type, help, required)

    Add a new argument to the plugin.

    :param short_name: the short name of the argument, eg. ``-a``.
    :type short_name: str
    :param long_name: (*optional*) the long name of the argument,
                      eg. ``--argument``.
    :type long_name: str
    :param dest: the name of the variable that will store the argument value.
    :type dest: str
    :param type: (*optional*) specify the type of the argument value.
                 Default to :class:`str`.
    :type type: built-in type
    :param help: the help message that describe this argument. Used by
                 ``--help``.
    :type help: str
    :param required: should this argument be required or not.
    :type required: bool

Looking to the help again with ``--help``::

 usage: my_super_plugin.py [-h] [--debug] [--version] -H HOSTNAME -a ARGUMENT

 Just a test with logging...

 optional arguments:
   -h, --help            show this help message and exit
   --debug               Show debug information, Nagios may truncate output
   --version             show program's version number and exit

 Plugin arguments:
   This arguments are required by the plugin.

   -H HOSTNAME           Target hostname (FQDN or IP address)
   -a ARGUMENT, --argument ARGUMENT
                        This is our new argument.

You can see ``-a or --argument`` in the default namespace named *Plugin
arguments*.

Getting the argument value in your plugin is done with the :attr:`options`
attribute of your plugin instance, which is here :data:`plugin`:
``plugin.options.<destvar>``.

Example::

 import logging
 from monitoring.nagios.plugin import NagiosPlugin

 logger = logging.getLogger('plugin')

 class MySuperPlugin(NagiosPlugin):
    def define_plugin_arguments(self):
        super(MySuperPlugin, self).define_plugin_arguments()

        self.required_args.add_argument('-a', '--argument',
                                        dest="argument",
                                        help="This is our new argument.",
                                        required=True)

 plugin = MySuperPlugin(version='1.0', description='Just a test with logging...')
 logger.debug('Show this message in debug mode only...')
 logger.debug('Value of argument: {0}'.format(plugin.options.argument))
 logger.debug('This is the end !')

Pre-defined argument types
..........................

.. module:: monitoring.nagios.plugin.argument

The library has support for arguments that are common in plugins such as
percent values, `Nagios thresholds
<https://nagios-plugins.org/doc/guidelines.html#THRESHOLDFORMAT>`_, time
related args, etc...

Everything is located within the module
:mod:`monitoring.nagios.plugin.argument`.

Reference them with the ``type`` keyword argument of :meth:`add_argument`.

**Example for a percent value argument**::

 ...

 from monitoring.nagios.plugin import argument

 ...

 self.required_args.add_argument('-u', '--used-space',
                                 dest="used_space",
                                 type=argument.percent,
                                 help="Used space threshold.",
                                 required=True)

Checkout all pre-defined argument types in :doc:`arguments`.

Nagios thresholds
.................

.. versionadded:: 1.3.1
        New argument type that add support for `Nagios Threshold
        <https://nagios-plugins.org/doc/guidelines.html#THRESHOLDFORMAT>`_
        format.

There is also support of `Nagios threshold format
<https://nagios-plugins.org/doc/guidelines.html#THRESHOLDFORMAT>`_ as described
in the Developer Guidelines by using the argument type
:class:`NagiosThreshold`.

The following code will create a warning argument that accept this format::

 ...

 from monitoring.nagios.plugin import argument

 ...

 self.required_args.add_argument('-w', '--warning',
                                 dest="used_space",
                                 type=argument.NagiosThreshold,
                                 help="Warning threshold.")

You can now test if the plugin must generate an alert with the
:meth:`NagiosThreshold.test` method::

 ...

 value = 54
 if plugin.options.warning.test(value):
    plugin.warning("A warning here !")
 elif plugin.options.critical.test(value):
    plugin.critical("Critical alert !!")
 else:
    plugin.ok("Nothing is going wrong here.")

Grouping arguments
..................

You can create others namespaces if needed. For example, one for thresholds,
modify the :meth:`define_plugin_arguments` to::

 def define_plugin_arguments(self):
     super(MySuperPlugin, self).define_plugin_arguments()

     args_thresholds_group = self.parser.add_argument_group("Thresholds", "Arguments for thresholds")
     args_thresholds_group.add_argument('-w',
                                        dest="warning",
                                        type=int,
                                        help="This is our warning threshold, an integer.",
                                        required=True)
     args_thresholds_group.add_argument('-c',
                                        dest="critical",
                                        type=int,
                                        help="This is our critical threshold, an integer.",
                                        required=True)

This will show in the help with ``--help``::

 Thresholds:
   Arguments for thresholds

   -w WARNING   This is our warning threshold, an integer.
   -c CRITICAL  This is our critical threshold, an integer.

Cool ?

Sanity checks on arguments
--------------------------

This is the same way as adding new arguments. You overrides
:meth:`verify_plugin_arguments` in your MySuperPlugin class. In
this method you will focus only on arguments verifications, one that is
typical::

 def verify_plugin_arguments(self):
     super(MySuperPlugin, self).verify_plugin_arguments()

     # Checking if warning thresholds is not > critical
     if self.options.warning > self.options.critical:
        self.unknown('Warning cannot be greater than critical !')

In this example, the plugin will exit with code 3 (UNKNOWN status) if the ``-w``
argument value (warning) is greater than ``-c`` argument value (critical)::

 $ python my_super_plugin.py -H fake_host -w 100 -c 50
 UNKNOWN - Warning cannot be greater than critical !

That's also cool, no ? ;-)

Output to Nagios
================

:class:`NagiosPlugin` class and inheritors have a list of attributes in order to
send output to Nagios and a status code:

Preparation
-----------

During plugin execution, you must prepare the following (do not use one if not
needed, for example the long output...). Assuming :data:`plugin` is your
instance if :class:`NagiosPlugin` or any other that inherits from it like the
examples above.

:attr:`shortoutput`

    This is a string containing the first line that Nagios will show in status
    information table or in alerts. You can use variable substitution here::

     plugin.shortoutput = "My name is {fullname}"

:attr:`longoutput`

    This is the extra lines that should be shown as long output in the Thruk
    popup. This is a list, append lines with::

     plugin.longoutput.append("A new line of long output")
     plugin.longoutput.append("Another one...")

:attr:`perfdata`

    A list of the datasources that are used in graphs. This is a list, append
    with::

     plugin.perfdata.append("data1=valueU;MIN;MAX;WARN;CRIT;")
     plugin.perfdata.append("data2=valueU;MIN;MAX;WARN;CRIT;")

Please note that variable substitution is working here for each attributes. For
example, with perfdata::

 plugin.perfdata.append('{table}={value}r;{warn};;0;'.format(warn=plugin.options.warning,
                                                            table=table_name.lower(),
                                                            value=num_rows))

Send the final output string to Nagios with :meth:`output` method.

.. py:method:: output([subs])

    Format the final string of text that will be send to Nagios. Includes short
    output, long output and performance data.

    :param subs: (*optional*) a keyword dict that will be used to replace *keys* by *values* in the final string.
    :type subs: dict

    :returns: the final string with variables substitued if any provided by subs.
    :rtype: str

Example::

 import logging
 from monitoring.nagios.plugin import NagiosPlugin

 logger = logging.getLogger('plugin')

 class MySuperPlugin(NagiosPlugin):
     pass

 plugin = MySuperPlugin(version='1.0', description='Just a test with logging...')
 plugin.shortoutput = "My name is {fullname}"

 subs = {
     'fullname': 'Vincent Besancon',
 }

 for i in range(1, 10):
     plugin.longoutput.append("Long output line n{0}.".format(i))
     plugin.perfdata.append("data{0}={0};".format(i))

 plugin.longoutput.append("Global substitution ! Hello Mr. {fullname} ;-)")

 print plugin.output(subs)

This will output::

 My name is Vincent Besancon
 Long output line n1.
 Long output line n2.
 Long output line n3.
 Long output line n4.
 Long output line n5.
 Long output line n6.
 Long output line n7.
 Long output line n8.
 Long output line n9.
 Global substitution ! Hello Mr. Vincent Besancon ;-) | data1=1; data2=2; data3=3; data4=4; data5=5; data6=6; data7=7; data8=8; data9=9;

To send a status to Nagios, 4 methods are availables: :meth:`ok`,
:meth:`warning`, :meth:`critical` and :meth:`unknown`. Just change the last line
to::

 plugin.ok(plugins.output(subs))

This will exit with code 0 for OK. We also prepend to
:attr:`shortoutput` the current status.

Plugin template
===============

Here is a template that you can use to create new plugin::

 #!/usr/bin/env python2.7
 # -*- coding: utf-8 -*-
 # Copyright (C) AUTHOR <ADDRESS>
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

 import logging
 import traceback
 
 from monitoring.nagios.plugin import NagiosPlugin
 
 
 # Initialize default logger
 logger = logging.getLogger("plugin.default")
 
 
 # Customize plugin here
 class CustomPlugin(NagiosPlugin):
     """
     Customize Plugin definition.
     """
     pass
 
 
 # Initialize the plugin
 plugin = CustomPlugin(version="1.0.0",
                       description="Parse JSON data via HTTP.")
 
 try:
     # Plugin execution code goes here.
     logger.debug("Plugin execution started...")
 except Exception:
     plugin.shortoutput = "Unexpected plugin behavior ! Traceback attached."
     plugin.longoutput = traceback.format_exc().splitlines()
     plugin.unknown(plugin.output())
