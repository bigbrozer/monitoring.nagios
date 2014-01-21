================
WMI based plugin
================

.. currentmodule:: monitoring.nagios.plugin

The class :class:`NagiosPluginWMI` that inherits from :class:`NagiosPlugin` is
responsible to init a plugin based on WMI.

She will provides new attributes and methods in order to query a host using
WMI.

If you show the help with ``--help``, you will see extra arguments provided by
the class. It uses the same mechanics as we saw in :doc:`new_plugin` section. It
overrides :meth:`NagiosPlugin.define_plugin_arguments` to define new arguments
and :meth:`NagiosPlugin.verify_plugin_arguments` to do arguments checking.

Getting started
===============

::

 import logging
 from monitoring.nagios.plugin import NagiosPluginSNMP

 logger = logging.getLogger('plugin')

 plugin = NagiosPluginWMI()
 system_infos = plugin.execute(r'SELECT * FROM Win32_OperatingSystem')

 for attribute in system_infos:
    print "Hostname: ", attribute['CSName']

- :data:`plugin` is a :class:`NagiosPluginWMI` instance.
- :data:`system_infos` is the result of :meth:`NagiosPluginWMI.execute` that
  returns a list of dict that contains the attributes (WMI columns) as the key
  and the associated value (``attribute['CSName']``).

If you enable DEBUG mode (with ``--debug``), you will have the result of the
query::

 [{None: ['5.2.3790', 'C:\\WINDOWS'],
  'BootDevice': '\\Device\\HarddiskVolume1',
  'BuildNumber': '3790',
  'BuildType': 'Uniprocessor Free',
  'CSCreationClassName': 'Win32_ComputerSystem',
  'CSDVersion': 'Service Pack 2',
  'CSName': 'WWGRPCTS6401',
  'Caption': 'Microsoft(R) Windows(R) XP Professional x64 Edition',
  'CodeSet': '1252',
  'CountryCode': '1',
  'CreationClassName': 'Win32_OperatingSystem',
  'CurrentTimeZone': '60',
  'DataExecutionPrevention_32BitApplications': 'True',
  'DataExecutionPrevention_Available': 'True',
  'DataExecutionPrevention_Drivers': 'True',
  'DataExecutionPrevention_SupportPolicy': '2',
  'Debug': 'False',
  'Description': 'Workstation NEMO',
 }, '...']

Notes
=====

- Some columns do not have a name, so the key is ``None``.
