"""Test DnsRecord Class."""
import unittest

from dbtobindzone.builders.dns_record import DnsRecord
from dbtobindzone.misc.exceptions import DnsRecordNotFound
from dbtobindzone.misc.exceptions import InvalidReferencesException


class TestDnsRecordCase(unittest.TestCase):
    """Test DnsRecord Class main case."""

    def test_str_method(self):
        """Test str method."""
        record = DnsRecord('com', 'example', '1.2.3.4')
        self.assertEqual(str(record), "example IN A 1.2.3.4")

    def test_name_with_zone(self):
        """Test domain name with fqdn."""
        record = DnsRecord('com', 'www.example.com', '1.2.3.4')
        self.assertEqual(record.zone, "com")
        self.assertEqual(record.domain_name, "www.example")
        self.assertEqual(str(record), "www.example IN A 1.2.3.4")

    def test_fqdn_with_zone(self):
        """Test fqdn of fqdn."""
        record = DnsRecord('com', 'www.example.com', '1.2.3.4')
        self.assertEqual(record.fqdn, "www.example.com")

    def test_fqdn_without_zone(self):
        """Test fqdn without zone."""
        record = DnsRecord('com', 'www.example', '1.2.3.4')
        self.assertEqual(record.fqdn, "www.example.com")

    def test_fqdn_of_alias(self):
        """Test fqnd of alias."""
        record = DnsRecord('com', 'www.example', '1.2.3.4')
        alias = DnsRecord('com', 'jopka', record)
        self.assertEqual(alias.fqdn, "jopka.com")

    def test_fqdn_of_alias_alias(self):
        """Test fqnd of alias of alias."""
        record = DnsRecord('com', 'example', '1.2.3.4')
        alias1 = DnsRecord('com', 'server.example', record)
        alias2 = DnsRecord('com', 'dev.server.example', alias1)
        self.assertEqual(alias2.fqdn, "dev.server.example.com")
        self.assertEqual(str(alias2), "dev.server.example IN CNAME "
                                      "server.example")

    def test_fqdn_of_alias_w_fqdn(self):
        """Test alias name ref to fqdn."""
        record = DnsRecord('com', 'www.example', '1.2.3.4')
        alias = DnsRecord('com', 'jopka.www.example.com', record)
        self.assertEqual(alias.fqdn, "jopka.www.example.com")
        self.assertEqual(str(alias), "jopka.www.example "
                         "IN CNAME www.example")

    def test_fqdn_of_alias_w_domain(self):
        """Test alias name refs parent name, without zone."""
        record = DnsRecord('com', 'www.example', '1.2.3.4')
        alias = DnsRecord('com', 'jopka.www.example', record)
        self.assertEqual(alias.fqdn, "jopka.www.example.com")
        self.assertEqual(str(alias), "jopka.www.example "
                         "IN CNAME www.example")

    def testzone_with_dot(self):
        """Test zone with dot."""
        record = DnsRecord('.com', 'www.example.com', '1.2.3.4')
        self.assertEqual(str(record), "www.example IN A 1.2.3.4")
        self.assertEqual(record.zone, "com")

    def test_dns_alias_str(self):
        """Test dns alias string."""
        record = DnsRecord('com', 'example.com', '1.2.3.4')
        alias = DnsRecord('com', 'www.example.com', record)
        self.assertEqual(str(alias), "www.example IN CNAME example")

    def test_dns_alias_str_third_lvl(self):
        """Test dns alias of alias string."""
        record = DnsRecord('com', 'example.com', '1.2.3.4')
        alias = DnsRecord('com', 'www.example.com', record)
        second_alias = DnsRecord('com', 'john.example.com', alias)
        self.assertEqual(str(second_alias),
                         "john.example IN CNAME www.example")

    def test_add_alias(self):
        """Test add_alias_method."""
        record = DnsRecord('com', 'example.com', '1.2.3.4')
        alias = record.add_alias('www.example.com')
        self.assertEqual(str(alias), "www.example IN CNAME example")
        megaserver_alias = alias.add_alias('megaserver.com')
        self.assertEqual(str(megaserver_alias),
                         "megaserver IN CNAME www.example")

    def test_add_subdomain(self):
        """Test subdomain method."""
        record = DnsRecord('com', 'example.com', '1.2.3.4')
        alias = record.add_subdomain('dev')
        self.assertEqual(str(alias), "dev.example IN CNAME example")
        alias_to_alias = alias.add_subdomain('www')
        self.assertEqual(str(alias_to_alias), "www.dev.example IN "
                                              "CNAME dev.example")

    def test_alias_to_subdomain(self):
        """Test alias to subdomain works."""
        record = DnsRecord('com', 'example.com', '1.2.3.4')
        subdomain = record.add_subdomain('dev')
        alias = subdomain.add_alias('mainserver.example.com')
        self.assertEqual(str(alias), "mainserver.example IN "
                                     "CNAME dev.example")

    def test_subdomain_to_alias(self):
        """Test subdomain to alias."""
        record = DnsRecord('com', 'example.com', '1.2.3.4')
        alias = record.add_alias('mainserver.example.com')
        subdomain = alias.add_subdomain('dev')
        self.assertEqual(str(subdomain), "dev.mainserver.example IN "
                                         "CNAME mainserver.example")

    def test_search_method(self):
        """Test search method."""
        record = DnsRecord('com', 'example.com', '1.2.3.4')
        alias = record.add_alias('mainserver.example.com')
        alias.add_subdomain('dev')
        result = record.search('dev.mainserver.example.com')
        self.assertEqual(result.fqdn, 'dev.mainserver.example.com')

    def test_search_same_record(self):
        """Test search same record."""
        record = DnsRecord('com', 'example.com', '1.2.3.4')
        same_record = record.search('example.com')
        self.assertEqual(record, same_record)
        self.assertEqual(id(record), id(same_record))

    def test_search_not_found(self):
        """Test search and not found."""
        record = DnsRecord('com', 'example.com', '1.2.3.4')
        with self.assertRaises(DnsRecordNotFound):
            record.search('some.data')


class TestDnsRecordConstructor(unittest.TestCase):
    """Test constructor and set_references method."""

    def test_constructor_fails(self):
        """Test constructor fails with not str, list."""
        with self.assertRaises(InvalidReferencesException):
            DnsRecord('com', 'example.com', 10)

    def test_constructor(self):
        """Test class constructor."""
        record = DnsRecord('com', 'example.com', '1.2.3.4')
        self.assertTrue(hasattr(record, 'zone'))
        self.assertTrue(hasattr(record, 'domain_name'))
        self.assertTrue(hasattr(record, 'references_to'))
        self.assertTrue(hasattr(record, 'fqdn'))
        self.assertTrue(hasattr(record, 'add_alias'))

    def test_ref_to_list_of_one(self):
        """Ref to list of one ip."""
        record = DnsRecord('com', 'example.com', ['1.2.3.4'])
        self.assertEqual(str(record), "example IN A 1.2.3.4")

    def test_ref_to_list_of_two(self):
        """Ref to list of two ip."""
        record = DnsRecord('com', 'example.com', ['1.2.3.4', '5.6.7.8'])
        self.assertEqual(str(record), "example IN A 1.2.3.4\n"
                                      "example IN A 5.6.7.8")
