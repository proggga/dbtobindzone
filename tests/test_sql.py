'''Test sql connection module'''
import unittest
from app.sql import SqlConnection
from _mysql_exceptions import OperationalError


class TestSqlConnector(unittest.TestCase):
    '''Test connectior class'''

    def test_sql_with_wrong_connection(self):
        '''test sql with wrong options'''

        connection = SqlConnection(host='8.8.8.8', user='anon',
                                   password='bad_bass',
                                   port=999, database='nodb')
        with self.assertRaises(OperationalError) as context_manager:
            self.assertEqual(connection.query('', '', timeout=1), ())
        self.assertEqual(str(context_manager.exception),
                         '(2003, \'Can\\\'t connect to MySQL server on '
                         '\\\'8.8.8.8\\\' (110 "Connection timed out")\')')
