"""Testing Data from db fetcher"""
import unittest
from app.data_fetcher import DataFetcher
from app.sql import SqlConnection
from mock import MagicMock


class TestDataFetcher(unittest.TestCase):
    """TestClass for DataFetcher"""

    def setUp(self):
        self.connection = SqlConnection()
        self.connection.query = MagicMock(return_value=())
        self.fetcher = DataFetcher(self.connection)

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
