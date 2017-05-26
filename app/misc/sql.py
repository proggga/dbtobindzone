"""Sql Connection module store connection options and make querys"""
# coding: utf-8
import MySQLdb
from MySQLdb.cursors import DictCursor


class SqlConnection(object):
    """Store SQL Connection to simplify connecting"""

    def __init__(self, **kwargs):
        self.host = kwargs.get('host')
        self.user = kwargs.get('user')
        self.password = kwargs.get('password')
        self.database = kwargs.get('database')
        self.port = kwargs.get('port')
        self.charset = kwargs.get('charset', 'utf8')

    def set_connection_options(self, **kwargs):
        """set options by kwargs"""

        self.host = kwargs.get('host')
        self.user = kwargs.get('user')
        self.password = kwargs.get('password')
        self.database = kwargs.get('database')
        self.port = kwargs.get('port')
        self.charset = kwargs.get('charset', 'utf8')

    def query(self, query, args=None, **kwargs):
        """try send query to database with connection options"""

        database_connection = MySQLdb.connect(
            host=self.host, user=self.user, passwd=self.password,
            db=self.database, port=self.port, charset='utf8',
            connect_timeout=kwargs.get('timeout', 3),
        )
        cursor = database_connection.cursor(DictCursor)
        rows_count = cursor.execute(query, args)
        data = cursor.fetchall()
        cursor.close()
        database_connection.commit()
        database_connection.close()
        return data if rows_count else ()
