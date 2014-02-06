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

"""MSSQL probe module."""

import logging as log

from monitoring.nagios.probes import Probe
from monitoring.nagios.plugin.exceptions import PluginError
import pymssql

logger = log.getLogger('monitoring.nagios.probes.mssql')


class ProbeMSSQL(Probe):
    """
    A MS SQL Server probe.

    :param host: The host to connect to.
    :type host: str
    :param username: Login user name.
    :type username: str
    :param password: Login user password.
    :type password: str
    :param database: Database to connect to, by default selects the database
    which is set as default for specific user.
    :type database: str
    :param query_timeout: Query timeout in seconds, default is 30 secs.
    :type query_timeout: int
    :param login_timeout: Timeout for connection and login in seconds, default
    is 15 secs.
    :type login_timeout: int
    """
    def __init__(self, host, username, password, database=None,
                 query_timeout=30, login_timeout=15):
        super(ProbeMSSQL, self).__init__(host)

        logger.debug('Establishing MS SQL server connection '
                     'to %s on database %s with user %s...',
                     host, database, username)
        try:
            self._db_connection = pymssql.connect(host=self._hostaddress,
                                                  user=username,
                                                  password=password,
                                                  database=database,
                                                  timeout=query_timeout,
                                                  login_timeout=login_timeout,
                                                  as_dict=True)
        except pymssql.Error as e:
            raise PluginError('Cannot connect to the database %s on server '
                              '%s !' % (database, host), "\n".join(list(e)))

    def _get_cursor(self):
        """
        Get connection cursor.

        :return: MSSQL Connection Cursor.
        :rtype: pymssql.Cursor
        """
        return self._db_connection.cursor()

    def execute(self, query):
        """
        Execute a SQL query.

        :param query: SQL query.
        :type query: str
        :return: pymssql.Cursor
        """
        try:
            cursor = self._get_cursor()
            cursor.execute(query)
            return cursor
        except pymssql.Error as e:
            raise PluginError('Error during query execution !\n'
                              'Query: %s' % query, e.message)

    def close(self):
        """Close the connection."""
        self._db_connection.close()
