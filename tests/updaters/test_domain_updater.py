"""Test DomainUpdater class with content in files."""
# coding: utf-8
import json
import os
import unittest

from app.updaters.domain_updater import DomainUpdater
import mock


class TestDomainUpdater(unittest.TestCase):
    """Test domainupdater class.."""

    def setUp(self):
        """Setups TestCase."""
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
                                            dns_dir='tests/test_work_dir/',
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
                                            cache_dir='tests/test_work_dir/')

    def test_domain_cache_update(self):
        """Test cache created and right format."""
        self.domain_updater.refresh_cache()
        self.assertTrue(os.path.exists(self.domain_updater.cache_file))
        content = ''
        with open(self.domain_updater.cache_file) as fhandler:
            content = fhandler.read()
        self.assertEqual(json.loads(content), list(self.domains))

    def test_create_zone_file(self):
        """Test file zone created with domains.."""
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

    def test_create_zone_file_ver2(self):
        """Test file zone created with domains.."""
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
