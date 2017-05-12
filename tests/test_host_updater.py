""" Test HostUpdater class with content in files"""
# coding: utf-8
import os
import unittest

from app.data_fetcher import DataFetcher
from app.host_updater import HostUpdater
from app.sql import SqlConnection
from mock import MagicMock


class TestHostUpdater(unittest.TestCase):
    """Test hostupdater class"""

    def assert_raises_with_messsage(self, msg, func, *args, **kwargs):
        """assert that check Exception raised and has certain message"""

        with self.assertRaises(Exception) as content_manager:
            func(*args, **kwargs)
        self.assertEqual(str(content_manager.exception), msg)

    def setUp(self):
        self.connection = SqlConnection()

        self.fetcher = DataFetcher(self.connection, is_inner_dns=True)
        self.data_host2_v1 = ({
            'name': 'server1.dmz', 'address': '10.0.0.1'
        }, {
            'name': 'server2.dmz', 'address': '10.0.0.2'
        })
        self.data_host2_v2 = ({
            'name': 'server1.dmz', 'address': '10.0.0.11'
        }, {
            'name': 'server2.dmz', 'address': '10.0.0.2'
        })
        self.data_host1 = ({
            'name': 'server1.dmz', 'address': '10.0.0.1'
        },)
        self.connection.query = MagicMock(return_value=self.data_host1)
        self.host_updater = HostUpdater(self.fetcher,
                                        dns_dir='/tmp/test_m/',
                                        zones=[''],
                                        cache_dir='/tmp/test_m/')

    def tearDown(self):
        if os.path.exists(self.host_updater.cache_file):
            os.remove(self.host_updater.cache_file)

    def test_cache_create(self):
        """Test refresh create config"""
        self.assertTrue(self.host_updater.refresh_cache())
        self.assertTrue(os.path.exists(self.host_updater.cache_file))

    def test_cache_change(self):
        """Test cache changed by other content"""
        self.assertTrue(self.host_updater.refresh_cache())

        self.connection.query = MagicMock(return_value=self.data_host2_v1)
        self.assertTrue(self.host_updater.refresh_cache())

    def test_cache_without_data_change(self):
        """Test cache not changed"""
        self.assertTrue(self.host_updater.refresh_cache())

        self.assertFalse(self.host_updater.refresh_cache())

    def test_cache_change_small_diff(self):
        """test data dont change after get small diff"""
        self.connection.query = MagicMock(return_value=self.data_host2_v1)
        self.assertTrue(self.host_updater.refresh_cache())

        self.connection.query = MagicMock(return_value=self.data_host2_v2)
        self.assertTrue(self.host_updater.refresh_cache())

    def test_cache_change_empty_data(self):
        """test cache create with empty data"""
        self.connection.query = MagicMock(return_value=())
        self.assertTrue(self.host_updater.refresh_cache())

    def test_update_zone(self):
        """test method update_zone genereate certain content"""
        self.host_updater.zones = ['example.org', 'nowhere.com']
        self.connection.query = MagicMock(return_value=self.data_host2_v1)
        self.host_updater.refresh_cache()
        self.assert_raises_with_messsage('zone "not exists" not found',
                                         self.host_updater.update_zone,
                                         'not exists')
        self.host_updater.update_zone('example.org')
        zone_file = os.path.join(self.host_updater.dns_dir,
                                 'example.org.hosts')
        self.assertTrue(os.path.exists(zone_file))
        zone_file_content = ''
        with open(zone_file) as fhandler:
            zone_file_content = [line.strip() for line in
                                 fhandler.read().split('\n')]
        self.assertEqual(zone_file_content,
                         ['$ORIGIN    example.org.',
                          '',
                          'server1    IN              A    10.0.0.1',
                          'server2    IN              A    10.0.0.2',
                          ''])
