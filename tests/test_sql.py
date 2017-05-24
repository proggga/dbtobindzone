"""Test sql connection module"""
import re
import unittest

from _mysql_exceptions import MySQLError
from app.sql import SqlConnection
import mock


class TestSqlConnector(unittest.TestCase):
    """Test connectior class"""

    def test_sql_with_wrong_connection(self):
        """test sql with wrong options"""

        connection = SqlConnection(host='8.8.8.8', user='anon',
                                   password='bad_bass',
                                   port=999, database='nodb')
        with self.assertRaises(MySQLError) as context_manager:
            self.assertEqual(connection.query('', '', timeout=1), ())
        exception = context_manager.exception
        self.assertTrue(re.match(r".*connect to MySQL server on.*8\.8\.8\.8.*",
                                 str(exception)))

    def test_sql_connect(self):
        """test sql connect method (big mock)"""
        connection = SqlConnection(host='8.8.8.8', user='anon',
                                   password='bad_bass',
                                   port=999, database='nodb')
        with mock.patch('app.sql.MySQLdb.connect') as connect_method:
            cursor = mock.Mock(name='cursor_object')
            cursor.execute.return_value = 2
            mock_data = (
                {'column1': 'data1'},
                {'column1': 'data2'},
            )
            cursor.fetchall.return_value = mock_data

            database = mock.Mock(name='connect_to_database')
            database.cursor.return_value = cursor

            connect_method.return_value = database

            data = connection.query('some sql query')
            self.assertEqual(data, mock_data)
            cursor.execute.assert_called_with('some sql query', None)

            cursor.execute.return_value = 0
            data = connection.query('sql that return empty', args=())
            cursor.execute.assert_called_with('sql that return empty', ())
            self.assertEqual(data, ())

    def test_set_connection_options(self):
        """Test method which set new connection options"""
        connection = SqlConnection(host='8.8.8.8', user='anon',
                                   password='bad_bass',
                                   port=999, database='nodb')
        self.assertEqual(connection.host, '8.8.8.8')
        self.assertEqual(connection.user, 'anon')
        self.assertEqual(connection.password, 'bad_bass')
        self.assertEqual(connection.port, 999)
        self.assertEqual(connection.database, 'nodb')
        self.assertEqual(connection.charset, 'utf8')

        connection.set_connection_options(host='1.1.1.1', user='johny',
                                          password='qwerty',
                                          port=1234, database='emptydb',
                                          charset='windows-1251')

        self.assertEqual(connection.host, '1.1.1.1')
        self.assertEqual(connection.user, 'johny')
        self.assertEqual(connection.password, 'qwerty')
        self.assertEqual(connection.port, 1234)
        self.assertEqual(connection.database, 'emptydb')
        self.assertEqual(connection.charset, 'windows-1251')
