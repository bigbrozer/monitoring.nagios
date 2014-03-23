=================
SNMP based plugin
=================

.. currentmodule:: monitoring.nagios.plugin

The class :class:`NagiosPluginSNMP` that inherits from :class:`NagiosPlugin` is
responsible to init a plugin based on SNMP.

She will provides new attributes and methods in order to query a host using
SNMP.

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

 oids = {
     'descr': '1.3.6.1.2.1.1.1.0',
     'contact': '1.3.6.1.2.1.1.4.0',
 }

 plugin = NagiosPluginSNMP(version="1.0", description="Get the system description and contact")
 snmpquery = plugin.snmp.get(oids)

 print "Descr: ", snmpquery['descr']
 print "Contact: ", snmpquery['contact']

:data:`plugin` is a :class:`NagiosPluginSNMP` instance.

.. attribute:: NagiosPluginSNMP.snmp

    Instance of :class:`ProbeSNMP`. Use :meth:`get` and pass it a dict with
    a name for your OID as the key and the OID string as the value. You can
    check for many OIDs as you want, just add their names and the OID string
    to the dict.

The :meth:`get` method returns a dict represented by :data:`snmpquery` with key as the name
you defined and as the value it will be the result of the SNMP get query. For
example here, the value of OID SysDescr (1.3.6.1.2.1.1.1) is available with
``snmpquery['descr']``.

