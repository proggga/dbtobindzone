"""Test DotConfig class"""
import unittest

from app.misc.dot_config import DotConfig


class TestDotConfigCase(unittest.TestCase):
    """DotConfig main TestCase"""

    def test_constructor(self):
        """test simple constructor"""
        config = DotConfig({})
        self.assertIsInstance(config, DotConfig)
        self.assertEqual(set(config.keys()), set([]))

    def test_constructor_without_args(self):
        """test simple constructor without args"""
        with self.assertRaises(TypeError):
            DotConfig()  # noqa # pylint: disable=no-value-for-parameter

    def test_constructor_with_bad_arg(self):
        """test simple constructor without args"""
        with self.assertRaises(TypeError):
            DotConfig('some string')

    def test_give_some_data(self):
        """test simple constructor without args"""
        config = DotConfig({'startup': True, 'clients': 10})
        self.assertEqual(set(config.keys()), set(['startup', 'clients']))
        self.assertEqual(config.startup, True)
        self.assertEqual(config.clients, 10)

    def test_dict_in_dics(self):
        """test get_attribute"""
        config = DotConfig({
            'parameters': {
                'clients': 10
            },
            'somekey': 'data',
        })
        self.assertIsInstance(config.parameters, DotConfig)
        self.assertIsInstance(config.parameters.clients, int)
        self.assertEqual(config.parameters.clients, 10)
        self.assertIsInstance(config.somekey, str)
        self.assertEqual(config.somekey, 'data')

    def test_getattr(self):
        """Test __getattr__ method"""
        config = DotConfig({
            'user': 'jack',
            'passwd': 'password1234',
        })
        self.assertEqual(config['user'], 'jack')
        self.assertEqual(config['passwd'], 'password1234')

    def test_getattr_failed(self):
        """Test key which not exists"""
        config = DotConfig({})
        with self.assertRaises(KeyError):
            config.some_key_not_exists()

    def test_str_method(self):
        """test get_attribute"""
        data = {
            'text': 'hello',
            'count': 10,
        }
        config = DotConfig(data)
        self.assertEqual(str(config), str(data))

    def test_load_fail_wrong_file(self):
        """test error when file not found"""
        with self.assertRaises(OSError):
            DotConfig.load('file does not exists')

    def test_load_from_bad_yml(self):
        """test load from bad yml file"""
        filename = 'tests/fixtures/test_incorrect_format.yml'
        message = ("Some error with file format in {} (should be YAML)"
                   .format(filename))
        with self.assertRaises(OSError) as contextmanager:
            DotConfig.load(filename)
        self.assertEqual(str(contextmanager.exception), message)

    def test_load_from_bad_file_content(self):
        """test load from bad yml file"""
        filename = 'tests/fixtures/test_incorrect_content.yml'
        message = ('Config {} is empty, or have not "config" block'
                   .format(filename))
        with self.assertRaises(OSError) as contextmanager:
            DotConfig.load(filename)
        self.assertEqual(str(contextmanager.exception), message)

    def test_load_from_good_file(self):
        """test load from yml file"""
        filename = 'tests/fixtures/test_correct.yml'
        config = DotConfig.load(filename)
        self.assertEqual(config.user, 'username')
        self.assertEqual(config.ask_password, False)
        self.assertEqual(config.connection.host, 'example.org')
        self.assertEqual(config.connection.port, 8080)
