"""Test builder interface"""
import unittest

from app.builders.builder import DnsBuilder


class TestBuilderTestCase(unittest.TestCase):
    """Test Builder TestCase"""

    def test_builder_is_abstact(self):
        """Test inteface is abstact"""
        with self.assertRaises(TypeError):
            DnsBuilder()  # pylint: disable=abstract-class-instantiated

    def test_builder_has_methods(self):
        """Test inteface is abstact"""
        self.assertTrue(hasattr(DnsBuilder, 'add_record'))
        self.assertTrue(hasattr(DnsBuilder, 'add_alias'))
        self.assertTrue(hasattr(DnsBuilder, 'get_result'))
