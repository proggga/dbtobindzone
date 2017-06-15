"""Testing Data from db fetcher."""
import unittest

from _mysql_exceptions import MySQLError
from dbtobindzone.fetcher.data_fetcher import DataFetcher
import mock


class TestDataFetcher(unittest.TestCase):
    """TestClass for HostDataFetcher."""

    def setUp(self):
        """Setups TestCase."""
        self.connection = mock.MagicMock()
        self.connection.query.return_value = 'some data'
        self.fetcher = DataFetcher(self.connection)
        self.get_query_mockpath = ('dbtobindzone.fetcher.data_fetcher'
                                   '.DataFetcher.get_query')

    def test_execute_method(self):
        """Test execute working."""
        with mock.patch(self.get_query_mockpath) as get_query:
            get_query.return_value = 'SQL-QUERY'
            self.fetcher.execute()
        self.connection.query.assert_called_with('SQL-QUERY', [])
        self.assertEqual(self.fetcher.get_data(), 'some data')

    def test_execute_raise_mysqlerror(self):
        """Test execute method  return 'not success'."""
        self.connection.query.side_effect = MySQLError('Some error with query')
        with mock.patch(self.get_query_mockpath) as get_query:
            get_query.return_value = 'SQL-QUERY'
            self.fetcher.execute()
        self.assertFalse(self.fetcher.is_fetch_success())

    def test_get_query_not_implented(self):
        """Test get query raise NotImplementedError."""
        with self.assertRaises(NotImplementedError):
            self.fetcher.get_query()
