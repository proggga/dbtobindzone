"""Test DnsRecord Class"""
import unittest

from app.builders.dns_record import DnsRecord


class TestDnsRecordCase(unittest.TestCase):
    """Test DnsRecord Class main case"""

    def test_constructor(self):
        """test class constructor"""
        record = DnsRecord('com', 'example.com', '1.2.3.4')
        self.assertTrue(hasattr(record, 'domain_name'))
        self.assertTrue(hasattr(record, 'references_to'))
        self.assertTrue(hasattr(record, 'add_alias'))

    def test_dns_record_str(self):
        """Test dns record string"""
        record = DnsRecord('com', 'example', '1.2.3.4')
        self.assertEqual(str(record), "example IN A 1.2.3.4")

    def test_dns_record_withzone(self):
        """Test dns record string"""
        record = DnsRecord('com', 'www.example.com', '1.2.3.4')
        self.assertEqual(str(record), "www.example IN A 1.2.3.4")

    def test_dns_alias_str(self):
        """Test dns alias string"""
        record = DnsRecord('com', 'example.com', '1.2.3.4')
        alias = DnsRecord('com', 'www.example.com', record)
        self.assertEqual(str(alias), "www.example IN CNAME example")

    def test_dns_alias_str_third_lvl(self):
        """Test dns alias of alias string"""
        record = DnsRecord('com', 'example.com', '1.2.3.4')
        alias = DnsRecord('com', 'www.example.com', record)
        second_alias = DnsRecord('com', 'john.example.com', alias)
        self.assertEqual(str(second_alias),
                         "john.example IN CNAME www.example")
