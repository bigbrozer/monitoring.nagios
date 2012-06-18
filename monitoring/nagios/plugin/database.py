# -*- coding: utf-8 -*-
#===============================================================================
# Filename      : monitoring.nagios.plugin.database
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : Class to define a plugin using a database.
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
import os
import sys

from monitoring.nagios.plugin.exceptions import PluginError
from monitoring.nagios.logger import debug_multiline
from monitoring.nagios.plugin import NagiosPlugin
from monitoring.nagios.probes import ProbeMSSQL

logger = log.getLogger('monitoring.nagios.plugin.database')


class NagiosPluginMSSQL(NagiosPlugin):
    """Base for a standard SSH Nagios plugin"""

    def __init__(self, name=os.path.basename(sys.argv[0]), version='', description=''):
        super(NagiosPluginMSSQL, self).__init__(name, version, description)

        # Init default plugin probe
        try:
            self.mssql = ProbeMSSQL(host=self.options.hostname,
                                username=self.options.username,
                                password=self.options.password,
                                database=self.options.database,
                                query_timeout=self.options.query_timeout,
                                login_timeout=self.options.login_timeout)
        except PluginError as e:
            self.critical(e)

        if 'NagiosPluginMSSQL' == self.__class__.__name__: logger.debug('=== END PLUGIN INIT ===')

    def define_plugin_arguments(self):
        """Define arguments for the plugin"""
        # Define common arguments
        super(NagiosPluginMSSQL, self).define_plugin_arguments()

        # Add extra arguments
        self.required_args.add_argument('-u', '--username',
                                        dest='username',
                                        help='Login user.',
                                        required=True)

        self.required_args.add_argument('-p', '--password',
                                        dest='password',
                                        help='Login user password.',
                                        required=True)

        self.required_args.add_argument('-d', '--database',
                                        dest='database',
                                        help='Database name.',
                                        required=True)

        self.required_args.add_argument('-qt', '--query-timeout',
                                        dest='query_timeout',
                                        type=int,
                                        default=30,
                                        help='Query timeout in seconds, default is 30 secs.',
                                        required=False)

        self.required_args.add_argument('-lt', '--login-timeout',
                                        dest='login_timeout',
                                        type=int,
                                        default=15,
                                        help='Timeout for connection and login in seconds, default is 15 secs.',
                                        required=False)

    def query(self, sql_query):
        """
        Execute a SQL query and fetch all data.

        :param sql_query: SQL query.
        :type sql_query: str
        :return: Results of the SQL query
        :rtype: list
        """
        logger.debug('Executing SQL query:')
        debug_multiline(sql_query)

        try:
            results = self.mssql.execute(sql_query)
            return results.fetchall()
        except PluginError as e:
            self.unknown(e)


if __name__ == '__main__':
    from pprint import pprint
    plugin = NagiosPluginMSSQL()
    pprint(plugin.query('SELECT * FROM gIMM.sys.sysfiles'))
