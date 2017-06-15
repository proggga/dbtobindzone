"""Testing Data from db fetcher."""
import unittest

from app.fetcher.host_data_fetcher import HostDataFetcher
import mock


class TestHostDataFetcher(unittest.TestCase):
    """TestClass for HostDataFetcher."""

    def setUp(self):
        """Setups TestCase."""
        self.connection = mock.MagicMock()
        self.connection.query.return_value = ()
        self.fetcher = HostDataFetcher(self.connection,
                                       ip_field='inIP',
                                       hostname_field='name',
                                       table='servers')

    def test_get_hosts(self):
        """Test get data by inner tag."""
        self.fetcher.execute()
        query = ('SELECT name as hostname, inIP as address'
                 ' from servers where status = 1')
        self.connection.query.assert_called_with(query, [])
