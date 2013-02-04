====================
Probes API reference
====================

.. module:: monitoring.nagios.probes

Reference for all probes.

------------------

Base class
==========

This is the base class for all plugin classes.

:mod:`base` --- Base class for all probes
-----------------------------------------

.. automodule:: monitoring.nagios.probes.base
    :members:
    :inherited-members:

Network protocols
=================

Plugins that interact with SNMP or SSH protocols.

:mod:`snmp` --- Probe to connect to a host using SNMP
-----------------------------------------------------

.. automodule:: monitoring.nagios.probes.snmp
    :members:
    :inherited-members:

:mod:`secureshell` --- Probe to connect to a host using SSH
-----------------------------------------------------------

.. automodule:: monitoring.nagios.probes.secureshell
    :members:
    :inherited-members:

:mod:`wmi` --- Probe to connect to a host using WMI
---------------------------------------------------

.. automodule:: monitoring.nagios.probes.wmi
    :members:
    :inherited-members:

Databases
=========

Plugins that interact with a database.

:mod:`mssql` --- Probe to connect to a Microsoft SQL Server
-----------------------------------------------------------

.. automodule:: monitoring.nagios.probes.mssql
    :members:
    :inherited-members:
