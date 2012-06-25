# -*- coding: utf-8 -*-
#===============================================================================
# Filename      : mssql
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : Module that define a MS SQL Server probe.
#-------------------------------------------------------------------------------
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

import logging as log

from monitoring.nagios.probes import Probe
from monitoring.nagios.plugin.exceptions import PluginError, NagiosUnknown, NagiosCritical
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
    :param database: Database to connect to, by default selects the database which is set as default for specific user.
    :type database: str
    :param query_timeout: Query timeout in seconds, default is 30 secs.
    :type query_timeout: int
    :param login_timeout: Timeout for connection and login in seconds, default is 15 secs.
    :type login_timeout: int
    """

    def __init__(self, host, username, password, database=None, query_timeout=30, login_timeout=15):
        super(ProbeMSSQL, self).__init__(host)

        logger.debug('Establishing MS SQL server connection to %s on database %s with user %s...' % (host, database,
                                                                                                     username))
        try:
            self._db_connection = pymssql.connect(host=self._hostaddress,
                                      user=username,
                                      password=password,
                                      database=database,
                                      timeout=query_timeout,
                                      login_timeout=login_timeout,
                                      as_dict=True)
        except pymssql.Error as e:
            raise PluginError('Cannot connect to the database %s on server %s !' % (database, host), e.message[1])

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
            raise PluginError('Error during query execution !\nQuery: %s' % query, e[1])
