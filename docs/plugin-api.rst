====================
Plugin API reference
====================

.. module:: monitoring.nagios.plugin

Reference for all classes.

------------------

Base class
==========

This is the base class for all plugin classes.

:class:`NagiosPlugin` --- Base class for all class plugin
---------------------------------------------------------

.. autoclass:: NagiosPlugin
    :members:

Network protocols
=================

Plugins that interact with SNMP or SSH protocols.

:class:`NagiosPluginSNMP` --- Plugin SNMP based
-----------------------------------------------

.. autoclass:: NagiosPluginSNMP
    :members:

:class:`NagiosPluginSSH` --- Plugin SSH based
---------------------------------------------

.. autoclass:: NagiosPluginSSH
    :members:

:class:`NagiosPluginWMI` --- Plugin WMI based
---------------------------------------------

.. autoclass:: NagiosPluginWMI
    :members:

:class:`NagiosPluginHTTP` --- Plugin HTTP based
-----------------------------------------------

.. autoclass:: NagiosPluginHTTP
    :members:

Databases
=========

Plugins that interact with a database.

:class:`NagiosPluginMSSQL` --- Plugin Microsoft SQL Server
----------------------------------------------------------

.. autoclass:: NagiosPluginMSSQL
    :members:
