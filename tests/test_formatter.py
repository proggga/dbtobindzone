'''
Test Foramming file with tabs
'''
import unittest

from app.formatter import Formatter


class TestFormatter(unittest.TestCase):
    '''Test Formmater case'''

    def test_sort_default(self):
        '''test sort default input'''
        result = Formatter.sort_by_column([
            ['serv1', 'in', 'A', '10.0.0.1'],
            ['fqdn.server2.org', 'in', 'A', '10.0.0.2']
        ])
        self.assertEqual(result, "serv1               in    A    10.0.0.1\n"
                                 "fqdn.server2.org    in    A    10.0.0.2\n")

    def test_sort_wrong_columns(self):
        '''test sort inpurt with wrong columns'''
        result = Formatter.sort_by_column([
            ['serv1', 'in', 'A', '10.0.0.1'],
            ['fqdn.server2.org']
        ])
        self.assertEqual(result, "serv1               in    A    10.0.0.1\n"
                                 "fqdn.server2.org\n")

    def test_sort_long_words(self):
        '''test sort input with wrong columns and long words'''
        result = Formatter.sort_by_column([
            ['serv1', 'in', 'A', '10.0.0.1'],
            ['fqdn.server2.org', 'word']
        ])
        self.assertEqual(result, "serv1               in      A    10.0.0.1\n"
                                 "fqdn.server2.org    word\n")

    def test_sort_empty_lines(self):
        '''test sort inpurt with empty line'''
        result = Formatter.sort_by_column([
            ['serv1', 'in', 'A', '10.0.0.1'],
            [],
            ['fqdn.server2.org', 'in', 'A', '10.0.0.2']
        ])
        self.assertEqual(result, "serv1               in    A    10.0.0.1\n"
                                 "\n"
                                 "fqdn.server2.org    in    A    10.0.0.2\n")

    def test_empty_line_wrong_columns(self):
        '''test sort inpurt with empty line and wrong columns'''
        result = Formatter.sort_by_column([
            ['serv1', 'in', 'A', '10.0.0.1'],
            [],
            ['fqdn.server2.org']
        ])
        self.assertEqual(result, "serv1               in    A    10.0.0.1\n"
                                 "\n"
                                 "fqdn.server2.org\n")

    def test_sort_empty_input(self):
        '''empty array is input for test'''
        result = Formatter.sort_by_column([])
        self.assertEqual(result, "")

    def test_sort_string(self):
        """test format simple example"""
        result = Formatter.sort_str_by_column("longword short same\n"
                                              "small longword same\n")
        self.assertEqual(result, "longword    short       same\n"
                                 "small       longword    same\n")

    def test_sort_str_with_spaces(self):
        """test format with many spaces in input"""
        result = Formatter.sort_str_by_column("  a   bbbb  \n"
                                              "ccc  ee   \n")
        self.assertEqual(result, "a      bbbb\n"
                                 "ccc    ee\n")

    def test_sort_str_with_many_newline(self):
        """test format with two new lines in input"""
        result = Formatter.sort_str_by_column("a b\n\ncc dd\n")
        self.assertEqual(result, "a     b\n"
                                 "\n"
                                 "cc    dd\n")

    def test_sort_str_with_tabs(self):
        """test format with tabs in input"""
        result = Formatter.sort_str_by_column("a\t\tb\ncc \t \tdd\n")
        self.assertEqual(result, "a     b\n"
                                 "cc    dd\n")
