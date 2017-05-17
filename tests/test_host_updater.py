""" Test HostUpdater class with content in files"""
# coding: utf-8
import os
import unittest

from app.fetcher.host_data_fetcher import HostDataFetcher
from app.exceptions import ZoneNotFoundException
from app.host_updater import HostUpdater
from app.sql import SqlConnection
import mock


class TestHostUpdater(unittest.TestCase):
    """Test hostupdater class"""

    def setUp(self):
        self.connection = SqlConnection()

        self.fetcher = HostDataFetcher(self.connection)
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
        self.connection.query = mock.MagicMock(return_value=self.data_host1)
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

        self.connection.query = mock.MagicMock(return_value=self.data_host2_v1)
        self.assertTrue(self.host_updater.refresh_cache())

    def test_cache_without_data_change(self):
        """Test cache not changed"""
        self.assertTrue(self.host_updater.refresh_cache())

        self.assertFalse(self.host_updater.refresh_cache())

    def test_cache_change_small_diff(self):
        """test data dont change after get small diff"""
        self.connection.query = mock.MagicMock(return_value=self.data_host2_v1)
        self.assertTrue(self.host_updater.refresh_cache())

        self.connection.query = mock.MagicMock(return_value=self.data_host2_v2)
        self.assertTrue(self.host_updater.refresh_cache())

    def test_cache_change_empty_data(self):
        """test cache create with empty data"""
        self.connection.query = mock.MagicMock(return_value=())
        self.assertTrue(self.host_updater.refresh_cache())

    def test_failed_with_unknown_zone(self):
        """Test update_zone raises ZoneNotFound"""
        with self.assertRaises(ZoneNotFoundException) as context_manager:
            self.host_updater.update_zone('not exists')
        self.assertEqual(str(context_manager.exception),
                         'zone "not exists" not found')

    def test_update_zone(self):
        """test method update_zone genereate certain content

        test looks close to integrity test
        """
        self.host_updater.zones = ['example.org', 'nowhere.com']
        self.connection.query = mock.MagicMock(return_value=self.data_host2_v1)
        self.host_updater.refresh_cache()
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

    def test_db_got_error_without_cache(self):
        """test database got error -> empty hosts list

        then mock fetcher fails when trying to get data
        from database and when cache not found should
        make empty list
        """
        mock_method_path = ('app.fetcher.host_data_fetcher'
                            '.HostDataFetcher.is_fetch_success')
        with mock.patch(mock_method_path) as mock_method:
            mock_method.return_value = False
            self.host_updater.refresh_cache()
        self.assertEqual(self.host_updater.hosts, [])

    def test_db_got_error(self):
        """test database got error -> loading from cache"""
        # update cache file from db
        self.host_updater.refresh_cache()
        # clean hosts for clean test
        self.host_updater.hosts = []
        # then mock fetcher fails when trying to get data from database
        # and refresh_cache should read from cache, not from db
        mock_method_path = ('app.fetcher.host_data_fetcher'
                            '.DataFetcher.is_fetch_success')
        with mock.patch(mock_method_path) as mock_method:
            mock_method.return_value = False
            self.host_updater.refresh_cache()
        self.assertEqual(self.host_updater.hosts, list(self.data_host1))

    def test_update_zones(self):
        """test update_zones"""
        self.host_updater.zones = ['zone1.ru', 'zone2.com']
        mock_method_path = 'app.host_updater.HostUpdater.update_zone'
        with mock.patch(mock_method_path) as mock_method:
            self.host_updater.update_zones()
            mock_method.assert_any_call('zone1.ru')
            mock_method.assert_any_call('zone2.com')

    def test_ref_cache_with_tempfile(self):
        """check existance of temp cachefile not broke system

        this file created for diff with current cache file
        """
        # update cache file from db
        self.host_updater.refresh_cache()
        # create temp_cache_file to test it doesnt broke system
        with open(self.host_updater.temp_cache_file, 'a'):
            pass
        self.host_updater.refresh_cache()
        self.assertFalse(os.path.exists(self.host_updater.temp_cache_file))

    def test_refresh_error_create_cache(self):
        """test exception block in refresh_cache in create block"""
        mock_method_path = 'app.host_updater.HostUpdater.cache_file'
        patch = mock.patch(mock_method_path, new_callable=mock.PropertyMock)
        with patch as mock_method:
            mock_method.return_value = '/TMP/DIR/NOT/EXISTS'
            result = self.host_updater.refresh_cache()
            self.assertFalse(result)

    def test_refresh_error_update_cache(self):
        """test exception block in refresh_cache in create block"""
        self.host_updater.refresh_cache()
        mock_method_path = 'app.host_updater.HostUpdater.temp_cache_file'
        patch = mock.patch(mock_method_path, new_callable=mock.PropertyMock)
        with patch as mock_method:
            mock_method.return_value = '/TMP/DIR/NOT/EXISTS'
            result = self.host_updater.refresh_cache()
            self.assertFalse(result)
