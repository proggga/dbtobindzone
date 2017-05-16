"""Testing Data from db fetcher"""
import unittest

from _mysql_exceptions import MySQLError
from app.data_fetcher import DataFetcher
from app.sql import SqlConnection
import mock


class TestDataFetcher(unittest.TestCase):
    """TestClass for DataFetcher"""

    def setUp(self):
        self.connection = SqlConnection()
        self.connection.query = mock.MagicMock(return_value=())
        self.fetcher = DataFetcher(self.connection)

    def test_fetcher_constructor(self):
        """test data fetcher constructor"""
        instance = DataFetcher(self.connection)
        self.assertTrue(instance.is_inner_dns)

        instance = DataFetcher(self.connection, is_inner_dns=False)
        self.assertFalse(instance.is_inner_dns)

    def test_get_hosts_by_inner_tag(self):
        """test get data by inner tag"""
        self.fetcher.is_inner_dns = True
        self.fetcher.get_hosts()
        query = 'SELECT name, inIP as address from hosts where status = 1'
        self.connection.query.assert_called_with(query, [])

    def test_get_hosts_by_external_tag(self):
        """test get data by external tag"""
        self.fetcher.is_inner_dns = False
        self.fetcher.get_hosts()
        query = 'SELECT name, outIP as address from hosts where status = 1'
        self.connection.query.assert_called_with(query, [])

    def test_get_domains_by_inner_tag(self):
        """test get domains by inner tag"""
        self.fetcher.is_inner_dns = True
        self.fetcher.get_domains()
        query = 'SELECT url, host, dns_servers as tag from aliases ' \
                'where dns_servers in ("both", "backup")'
        self.connection.query.assert_called_with(query, [])

    def test_get_domains_by_ext_tag(self):
        """test get domains by external tag"""
        self.fetcher.is_inner_dns = False
        self.fetcher.get_domains()
        query = 'SELECT url, host, dns_servers as tag from aliases ' \
                'where dns_servers in ("both", "moscow")'
        self.connection.query.assert_called_with(query, [])

    def test_execute_raise_mysqlerror(self):
        """test execute method not working"""
        self.connection.query = mock.Mock()
        self.connection.query.side_effect = MySQLError('Some error with query')
        self.fetcher.get_domains()
        self.assertFalse(self.fetcher.is_fetch_success())
