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

"""Database plugin module."""

from __future__ import division
import logging as log

from monitoring.nagios.exceptions import PluginError
from monitoring.nagios.logger import debug_multiline
from monitoring.nagios.plugin import NagiosPlugin
from monitoring.nagios.probes import ProbeMSSQL

logger = log.getLogger('monitoring.nagios.plugin.database')


#TODO: write tests for this class.
class NagiosPluginMSSQL(NagiosPlugin):
    """Base for a standard SSH Nagios plugin"""
    def __init__(self, *args, **kwargs):
        super(NagiosPluginMSSQL, self).__init__(*args, **kwargs)

        # Init default plugin probe
        try:
            self.mssql = ProbeMSSQL(hostaddress=self.options.hostname,
                                    username=self.options.username,
                                    password=self.options.password,
                                    database=self.options.database,
                                    query_timeout=self.options.query_timeout,
                                    login_timeout=self.options.login_timeout)
        except PluginError as e:
            self.critical(e)

        if 'NagiosPluginMSSQL' == self.__class__.__name__:
            logger.debug('=== END PLUGIN INIT ===')

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
                                        help='Query timeout in seconds, '
                                             'default is 30 secs.',
                                        required=False)

        self.required_args.add_argument('-lt', '--login-timeout',
                                        dest='login_timeout',
                                        type=int,
                                        default=15,
                                        help='Timeout for connection and '
                                             'login in seconds, default is '
                                             '15 secs.',
                                        required=False)

    def query(self, sql_query):
        """
        Execute a SQL query and fetch all data.

        :param sql_query: SQL query.
        :type sql_query: str, unicode
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

    def get_db_size(self):
        """
        Get the size of the database connected on. Also return the used
        percent. This returns a dict with a key per filename (eg. db.Data /
        db.Log) that is also a dict with keys 'size', 'maxsize' and 'used'
        (sizes are in bytes and used in percent).

        :return: dict
        """
        query = self.query(
            r"""SELECT TOP 1000
            [file_id] ,[type_desc] ,[name] ,[state_desc] ,[size] ,[max_size]
            FROM [{0.database}].[sys].[database_files]""".format(self.options))
        db_size = {}
        for result in query:
            db_size[result['name']] = {
                'type': result['type_desc'].lower(),
                'size': result['size'],
                'maxsize': result['max_size'],
                'used': result['size'] / result['max_size'] * 100
                if result['max_size'] > 0 else None,
            }

        return db_size

    def get_all_db_status(self):
        """
        Query the status of all databases on the connected SQL Server.

        Return a list of tuples [(db_name, db_state), ...].

        :return: list(tuple)
        """
        query_result = self.query(
            r"""SELECT db.name, db.create_date, db.collation_name,
            db.state_desc, sdb.filename
            FROM sys.databases db
            JOIN sys.sysdatabases sdb ON db.database_id = sdb.dbid""")

        db_states = [(db['name'], db['state_desc']) for db in query_result]
        return db_states

    def get_server_time(self):
        """
        Return the local time of the SQL server.

        :return: local time of SQL server
        :rtype: datetime
        """
        server_datetime = self.query(
            r"SELECT GETDATE() AS ServerDateTime")[0]['ServerDateTime']
        return server_datetime

    def close(self):
        """Close the database connection."""
        self.mssql.close()
