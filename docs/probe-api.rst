====================
Probes API reference
====================

.. module:: monitoring.nagios.probes

Reference for all probes.

------------------

Base class
==========

This is the base class for all plugin classes.

:class:`Probe` --- Base class for all probes
--------------------------------------------

.. autoclass:: Probe
    :members:

Network protocols
=================

Plugins that interact with SNMP or SSH protocols.

:class:`ProbeSNMP` --- Probe to connect to a host using SNMP
------------------------------------------------------------

.. autoclass:: ProbeSNMP
    :members:
    :inherited-members:

:class:`ProbeSSH` --- Probe to connect to a host using SSH
----------------------------------------------------------

.. autoclass:: ProbeSSH
    :members:
    :inherited-members:

:class:`ProbeWMI` --- Probe to connect to a host using WMI
----------------------------------------------------------

.. autoclass:: ProbeWMI
    :members:
    :inherited-members:

Databases
=========

Plugins that interact with a database.

:class:`ProbeMSSQL` --- Probe to connect to a Microsoft SQL Server
------------------------------------------------------------------

.. autoclass:: ProbeMSSQL
    :members:
    :inherited-members:
