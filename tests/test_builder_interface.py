"""Test builder interface"""
import unittest

from app.builder import DnsBuilder


class TestBuilderTestCase(unittest.TestCase):
    """Test Builder TestCase"""

    def test_builder_is_abstact(self):
        """Test inteface is abstact"""
        try:
            DnsBuilder()  # pylint: disable=abstract-class-instantiated
            self.fail()
        except TypeError:
            pass

    def test_builder_has_methods(self):
        """Test inteface is abstact"""
        self.assertTrue(hasattr(DnsBuilder, 'add_record'))
        self.assertTrue(hasattr(DnsBuilder, 'add_alias'))
        self.assertTrue(hasattr(DnsBuilder, 'get_result'))
