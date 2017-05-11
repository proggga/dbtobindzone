''' Test HostUpdater class with content in files'''
# coding: utf-8
import os
import unittest

from app.fetcher import DataFetcher
from app.host_updater import HostUpdater
from app.sql import SqlConnection
from mock import MagicMock


class TestHostUpdater(unittest.TestCase):
    '''Test hostupdater class'''

    def setUp(self):
        self.connection = SqlConnection()
        self.fetcher = DataFetcher(self.connection, is_inner_dns=True)
        self.data_2host_ver1 = ({
            'name': 'server1.dmz', 'address': '10.0.0.1'
        }, {
            'name': 'server2.dmz', 'address': '10.0.0.2'
        })
        self.data_2host_ver2 = ({
            'name': 'server10.dmz', 'address': '10.0.0.10'
        }, {
            'name': 'server2.dmz', 'address': '10.0.0.2'
        })
        self.data_1host = ({
            'name': 'server1.dmz', 'address': '10.0.0.1'
        })

    def assert_raises_with_messsage(self, msg, func, *args, **kwargs):
        '''assert that check Exception raised and has certain message'''

        with self.assertRaises(Exception) as content_manager:
            func(*args, **kwargs)
        self.assertEqual(str(content_manager.exception), msg)

    def test_refresh_cache_for_inner(self):
        '''Test refresh state with custom content'''

        host_updater = HostUpdater(self.fetcher,
                                   dns_dir='/tmp/test_m/',
                                   zones=[''],
                                   cache_dir='/tmp/test_m/')

        if os.path.exists(host_updater.cache_file):
            os.remove(host_updater.cache_file)

        self.connection.query = MagicMock(return_value=self.data_2host_ver1)
        self.assertTrue(host_updater.refresh_cache())

        self.connection.query = MagicMock(return_value=self.data_1host)
        self.assertTrue(host_updater.refresh_cache())

        self.assertFalse(host_updater.refresh_cache())

        self.connection.query = MagicMock(return_value=self.data_2host_ver1)
        self.assertTrue(host_updater.refresh_cache())

        self.connection.query = MagicMock(return_value=self.data_2host_ver1)
        self.assertFalse(host_updater.refresh_cache())

        self.connection.query = MagicMock(return_value=self.data_2host_ver2)
        self.assertTrue(host_updater.refresh_cache())

        self.connection.query = MagicMock(return_value=())
        self.assertTrue(host_updater.refresh_cache())

        self.connection.query = MagicMock(return_value=())
        self.assertFalse(host_updater.refresh_cache())

        os.remove(host_updater.cache_file)

    def test_update_zone(self):
        '''test method update_zone genereate certain content'''
        host_updater = HostUpdater(self.fetcher,
                                   dns_dir='/tmp/test_m/',
                                   zones=['example.org', 'nowhere.com'],
                                   cache_dir='/tmp/')
        self.connection.query = MagicMock(return_value=self.data_2host_ver1)
        host_updater.refresh_cache()
        self.assert_raises_with_messsage('zone "not exists" not found',
                                         host_updater.update_zone,
                                         'not exists')
        host_updater.update_zone('example.org')
        zone_file = os.path.join(host_updater.dns_dir, 'example.org.hosts')
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
