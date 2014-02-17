====================
Probes API reference
====================

#.. module:: monitoring.nagios.probes

API Reference for all probes.

Base class
==========

This is the base class for all plugin classes.

.. automodule:: monitoring.nagios.probes.base
    :members:
    :inherited-members:

Network protocols
=================

Plugins that interact with SNMP or SSH protocols.

SNMP
------

.. automodule:: monitoring.nagios.probes.snmp
    :members:
    :inherited-members:

SSH
------

.. automodule:: monitoring.nagios.probes.secureshell
    :members:
    :inherited-members:

WMI
------

.. automodule:: monitoring.nagios.probes.wmi
    :members:
    :inherited-members:

HTTP
------

.. automodule:: monitoring.nagios.probes.http
    :members:
    :inherited-members:

Databases
=========

Plugins that interact with a database.

Microsoft SQL Server
--------------------

.. automodule:: monitoring.nagios.probes.mssql
    :members:
    :inherited-members:
