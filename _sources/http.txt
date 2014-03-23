=================
HTTP based plugin
=================

.. currentmodule:: monitoring.nagios.plugin

The class :class:`NagiosPluginHTTP` that inherits from :class:`NagiosPlugin` is
responsible to init a plugin based on HTTP requests.

She will provides new attributes and methods in order to query a host using
HTTP.

If you show the help with ``--help``, you will see extra arguments provided by
the class. It uses the same mechanics as we saw in :doc:`new_plugin` section. It
overrides :meth:`NagiosPlugin.define_plugin_arguments` to define new arguments
and :meth:`NagiosPlugin.verify_plugin_arguments` to do arguments checking.

Getting started
===============

Instanciate a new HTTP plugin with::

 >>> import logging
 >>> from monitoring.nagios.plugin import NagiosPluginHTTP

 >>> logger = logging.getLogger('plugin')

 >>> plugin = NagiosPluginHTTP(version="1.0",
 >>>                           description="Get a file from HTTP.")

Default plugin arguments
========================

The class defines the following default set of arguments.

- ``-H``: The hostaddress of the server to connect on.
- ``-p, --port``: on which port HTTP session is established (default to 80).
- ``-S, --ssl``: if we should use SSL (default No).
- ``-a, --auth``: A string for doing basic HTTP auth like login:passwd.

Making requests
===============

Make use of ``plugin.http`` attribute to make queries. This is an instance of
:class:`monitoring.nagios.probes.http.ProbeHTTP`.

.. note::
   All URL paths are relative to the hostaddress given with argument ``-H``.

Doing a HTTP GET query is simple as::

 >>> response = plugin.http.get("/file.json")

Checkout more details in :meth:`monitoring.nagios.probes.http.ProbeHTTP.get`.

Doing a HTTP POST query is simple as::

 >>> response = plugin.http.post("/post_path", data={"var1": "toto", "var2": "tata"})

This will post the ``data`` to the ``/post_path`` URL.

Playing with response
=====================

The ``response`` object now contains the server answer that makes new
attributes available to you in order to process server response. This is an
instance of :class:`monitoring.nagios.probes.http.HTTPResponse`

Response content
----------------

You can have the full server response (ex. HTML) using the ``content``
attribute::

 >>> print response.content
 '<HTML>
  ...
  ...'

JSON output
-----------

If the response returned by the server is JSON data, you can parse it to Python
objects like so::

 >>> json_data = response.json()
 >>> json_data
 [{u'repository': {u'open_issues': 0, u'url': 'https://github.com/...

You will obtain formatted object usable for Python. ``response.json()``
will raise a ``ValueError`` exception if any error occurs.

XML output
----------

If the response returned by the server is XML data, you can obtain a
``BeautifulSoup`` parser object and play with it like so::

 # Find all tags "<alert></alert>" in XML results
 >>> xml_data = response.xml()
 >>> xml_data.find_all("alert")

 # Get a last_update value using attributes like in XML
 # "<alert><last_update>10:00</last_update></alert>"
 >>> xml_data.alert.last_update
 '10:00'

Check out the documentation of
`BeautifulSoup 4 <http://www.crummy.com/software/BeautifulSoup/bs4/doc/>`_ for
more information about the available methods and attributes.