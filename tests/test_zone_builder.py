"""ZoneBuilder -> creates file by builder interface"""
import unittest

from app.exceptions import InvalidZone
from app.zone_builder import ZoneBuilder


class TestZoneBuilderConstandStatic(unittest.TestCase):
    """Test builder class constructor and static methods"""

    def test_constructor_no_args(self):
        """test contstructor fails without zone name"""
        with self.assertRaises(TypeError):
            ZoneBuilder()  # pylint: disable=no-value-for-parameter

    def test_check_zone_bad_zone(self):
        """test contstructor fails without zone name"""
        with self.assertRaises(InvalidZone):
            ZoneBuilder.check_zone('some zone')
        with self.assertRaises(InvalidZone):
            ZoneBuilder.check_zone('another.one-')

    def test_check_zone_good_zone(self):
        """Test check_zone method

        THIS METHODS SHOULD NOT RAISE InvalidZone exception
        """
        try:
            ZoneBuilder.check_zone('dmz')
            ZoneBuilder.check_zone('domain.ru')
            ZoneBuilder.check_zone('right.kodeks.net')
        except InvalidZone:  # pragma: no cover
            self.fail('InvalidZone catch, it is wrong')  # pragma: no cover

    def test_constructor(self):
        """Test constructor and zone property"""
        zone_name = 'example.com'
        builder = ZoneBuilder(zone_name)
        self.assertTrue(hasattr(builder, 'zone'))
        self.assertEqual(builder.zone, zone_name)


class TestZoneBuilderCase(unittest.TestCase):
    """Test builder class instanse methods"""

    def setUp(self):
        self.zone = 'example.com'
        self.builder = ZoneBuilder(self.zone)
        self.record_site = {
            'hostname': 'site',
            'address': '1.2.3.4',
        }
        self.record_mail = {
            'hostname': 'mail.example.com',
            'address': '5.6.7.8',
        }
        self.record_vpn = {
            'hostname': 'vpn.example.another.domain',
            'address': '91.56.33.251',
        }
        self.record_site_two = {
            'hostname': 'site',
            'address': '8.8.8.8',
        }
        self.alias_site = {
            'hostname': 'demo',
            'address': 'site.example.com',
        }

    def test_empty_get_data(self):
        """Test empty data"""
        result = self.builder.get_result()
        self.assertEqual(result, '$ORIGIN    example.com.\n')

    def test_add_record(self):
        """Test add_record method"""
        self.builder.add_record(self.record_site)
        result = self.builder.get_result()
        self.assertEqual(result, '$ORIGIN    example.com.\n'
                                 'site       IN              A    1.2.3.4\n')

    def test_flush_data(self):
        """Test empty data"""
        self.builder.add_record(self.record_site)
        result = self.builder.get_result()
        self.assertEqual(result, '$ORIGIN    example.com.\n'
                                 'site       IN              A    1.2.3.4\n')
        self.builder.flush_result()
        result = self.builder.get_result()
        self.assertEqual(result, '$ORIGIN    example.com.\n')

    def test_add_alias_to_non_exist(self):
        """Add alias to host which not exists in db (may be hardcoded)"""
        self.builder.add_alias(self.alias_site)
        result = self.builder.get_result()
        self.assertEqual(result, '$ORIGIN    example.com.\n'
                                 'demo       IN              '
                                 'CNAME    site.example.com.\n')

    def test_add_alias_to_exist_host(self):
        """Add alias to host which not exists in db (may be hardcoded)"""
        self.builder.add_record(self.record_site)
        self.builder.add_alias(self.alias_site)
        result = self.builder.get_result()
        self.assertEqual(result, '$ORIGIN    example.com.\n'
                                 'site       IN              A        '
                                 '1.2.3.4\n'
                                 'demo       IN              CNAME    '
                                 'site\n')

    def test_add_two_records_with_same(self):
        """Add another ip to same name"""
        self.builder.add_record(self.record_site)
        self.builder.add_record(self.record_site_two)
        self.builder.add_record(self.record_site_two)
        result = self.builder.get_result()
        self.assertEqual(result, '$ORIGIN    example.com.\n'
                                 'site       IN              A    '
                                 '1.2.3.4\n'
                                 'site       IN              A    '
                                 '8.8.8.8\n')

    @unittest.skip("Need rebuild builder to work this -> make Composite"
                   "A and CNAME Record Composite class")
    def test_two_same_aliases(self):
        """Add alias to host which not exists in db (may be hardcoded)"""
        self.builder.add_record(self.record_site)
        self.builder.add_alias(self.alias_site)
        self.builder.add_alias(self.alias_site)
        result = self.builder.get_result()
        self.assertEqual(result, '$ORIGIN    example.com.\n'
                                 'site       IN              A        '
                                 '1.2.3.4\n'
                                 'demo       IN              CNAME    '
                                 'site\n')

    @unittest.skip("Need rebuild builder to work this -> make Composite"
                   "A and CNAME Record Composite class")
    def test_two_aliases_wrong_order(self):
        """Add alias to host which not exists in db (may be hardcoded)"""
        self.builder.add_alias(self.alias_site)
        self.builder.add_record(self.record_site)
        result = self.builder.get_result()
        self.assertEqual(result, '$ORIGIN    example.com.\n'
                                 'site       IN              A        '
                                 '1.2.3.4\n'
                                 'demo       IN              CNAME    '
                                 'site\n')
