""" Test DomainUpdater class with content in files"""
# coding: utf-8
import unittest

import os
# from app.exceptions import ZoneNotFoundException
from app.domain_updater import DomainUpdater
import mock
import json


class TestDomainUpdater(unittest.TestCase):
    """Test domainupdater class"""

    def setUp(self):
        self.domains = ({
            'url': 'site1.example.ru',
            'host': 'server1.dmz',
            'tag': 'internal',
        }, {
            'url': 'site2.example.com',
            'host': 'server2.dmz',
            'tag': 'external',
        }, {
            'url': 'site3.example.ru',
            'host': 'server3.dmz',
            'tag': 'any',
        }, )

        self.fetcher = mock.MagicMock()
        self.fetcher.get_data.return_value = self.domains
        self.domain_updater = DomainUpdater(self.fetcher,
                                            dns_dir='/tmp/test_m/',
                                            zones={
                                                'example.ru': [
                                                    'any',
                                                    'internal'
                                                ],
                                                'example.com': [
                                                    'any',
                                                    'internal'
                                                ],
                                            },
                                            cache_dir='/tmp/test_m/')

    def test_domain_cache_update(self):
        '''test cache created and right format'''
        self.domain_updater.refresh_cache()
        self.assertTrue(os.path.exists(self.domain_updater.cache_file))
        content = ''
        with open(self.domain_updater.cache_file) as fhandler:
            content = fhandler.read()
        self.assertEqual(json.loads(content), list(self.domains))

    def test_create_zone_file(self):
        """test file zone created with domains"""
        zone = 'example.ru'
        self.domain_updater.update_zone(zone)
        content = ''
        with open(self.domain_updater.get_zone_file(zone)) as fhandler:
            content = fhandler.read()
        self.assertEqual(content, "$ORIGIN             example.ru.\n"
                                  "\n"
                                  "site1.example.ru    IN             "
                                  "CNAME    server1\n"
                                  "site3.example.ru    IN             "
                                  "CNAME    server3\n")

    def test_create_zone_file_second_version(self):
        """test file zone created with domains"""
        self.domain_updater.refresh_cache()
        self.assertTrue(os.path.exists(self.domain_updater.cache_file))
        zone = 'example.com'
        self.domain_updater.update_zone(zone)
        content = ''
        with open(self.domain_updater.get_zone_file(zone)) as fhandler:
            content = fhandler.read()
        self.assertEqual(content, "$ORIGIN              example.com.\n"
                                  "\n"
                                  "site2.example.com    IN              "
                                  "CNAME    server2\n")
