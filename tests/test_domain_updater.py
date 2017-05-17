""" Test DomainUpdater class with content in files"""
# coding: utf-8
import os
import unittest

from app.exceptions import ZoneNotFoundException
from app.domain_updater import DomainUpdater
import mock


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
        self.data_hosts_internal = ({
            'name': 'server1.dmz', 'address': '10.0.0.11'
        }, {
            'name': 'server2.dmz', 'address': '10.0.0.2'
        })
        self.data_hosts_external = ({
            'name': 'server1.dmz', 'address': '8.8.8.8'
        }, {
            'name': 'server2.dmz', 'address': '9.9.9.9'
        })

    #     self.fetcher = mock.MagicMock()
    #     self.fetcher.get_hosts.return_value = self.data_hosts_internal
    #     self.fetcher.get_domains.return_value = self.data_hosts_internal
    #     self.domain_updater = DomainUpdater(self.fetcher,
    #                                         tags=[
    #                                             'any',
    #                                             'inner'
    #                                         ],
    #                                         dns_dir='/tmp/test_m/',
    #                                         zones=[
    #                                             'example.ru',
    #                                             'example.com',
    #                                         ],
    #                                         cache_dir='/tmp/test_m/')
    #
    # def tearDown(self):
    #     if os.path.exists(self.domain_updater.cache_file):
    #         os.remove(self.domain_updater.cache_file)
