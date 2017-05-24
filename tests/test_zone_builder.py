"""ZoneBuilder -> creates file by builder interface"""
import unittest
from app.zone_builder import ZoneBuilder
from app.exceptions import InvalidZone


class TestZoneBuilderCase(unittest.TestCase):
    """Test builder class"""

    def test_constructor_no_args(self):
        """test contstructor fails without zone name"""
        with self.assertRaises(TypeError):
            ZoneBuilder()  # pylint: disable=no-value-for-parameter

    def test_constructor_bad_zone(self):
        """test contstructor fails without zone name"""
        with self.assertRaises(InvalidZone):
            ZoneBuilder('some zone')
        ZoneBuilder('dmz')

    def test_constructor(self):
        """Test constructor and zone property"""
        zone_name = 'example.com'
        builder = ZoneBuilder(zone_name)
        self.assertTrue(hasattr(builder, 'zone'))
        self.assertEqual(builder.zone, zone_name)
