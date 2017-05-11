"""Testing Data from db fetcher"""
import unittest
from app.fetcher import DataFetcher
from app.sql import SqlConnection
from mock import MagicMock


class TestDataFetcher(unittest.TestCase):
    """TestClass for DataFetcher"""

    def test_get_hosts_by_inner_location(self):
        """test get data by inner location"""
        connection = SqlConnection()
        connection.query = MagicMock(return_value=())
        fetcher = DataFetcher(connection, is_inner_dns=True)
        fetcher.get_hosts()
        query = 'SELECT name, inIP as address from hosts where status = 1'
        connection.query.assert_called_with(query, [])

    def test_get_hosts_by_external_location(self):
        """test get data by external location"""
        connection = SqlConnection()
        connection.query = MagicMock(return_value=())
        fetcher = DataFetcher(connection, is_inner_dns=False)
        fetcher.get_hosts()
        query = 'SELECT name, outIP as address from hosts where status = 1'
        connection.query.assert_called_with(query, [])
