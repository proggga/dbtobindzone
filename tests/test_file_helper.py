"""FileHelper class test"""
import unittest

from app.file_helper import FileHelper


class TestFileHelper(unittest.TestCase):
    """TestCase for FileHelper"""

    def setUp(self):
        self.file_not_exists = 'file not exists here'
        self.file1 = 'tests/fixtures/fh_file1.txt'
        self.file2 = 'tests/fixtures/fh_file2.txt'

    def test_samefiles(self):
        """test one file, should be same"""
        files_same = FileHelper.equal(self.file1, self.file1)
        self.assertTrue(files_same)

        files_same = FileHelper.differ(self.file1, self.file1)
        self.assertFalse(files_same)

    def test_diff_files(self):
        """test two files, should differ"""
        files_same = FileHelper.equal(self.file1, self.file2)
        self.assertFalse(files_same)

        files_diff = FileHelper.differ(self.file1, self.file2)
        self.assertTrue(files_diff)

    def test_not_exists_files(self):
        """test file which not exists"""
        with self.assertRaises(EnvironmentError):
            FileHelper.differ(self.file_not_exists, self.file1)
        with self.assertRaises(EnvironmentError):
            FileHelper.differ(self.file1, self.file_not_exists)
