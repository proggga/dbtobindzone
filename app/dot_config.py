'''Module allow load yaml config to object, accessed by dot

Allow create yaml config and load, easy access to childs and data by dots
like Example:
config = DotConfig.load('filename')
config.key.list # item1, item2
'''
# coding: utf-8
import os
import yaml


class DotConfig(object):
    '''Config object accessed by dots'''

    def __init__(self, cfg):
        self._cfg = cfg

    def __getattr__(self, key):
        '''Get attr from dictionary or method'''

        data = self._cfg[key]
        if isinstance(data, dict):
            return DotConfig(data)
        return data

    def __str__(self):
        return str(self._cfg)

    def keys(self):
        '''return keys of inner dict'''

        return self._cfg.keys()

    def __getitem__(self, item):
        return self._cfg.__getitem__(item)

    @classmethod
    def load(cls, filename):
        '''load file from yaml and return loaded DotConfig'''

        if not os.path.exists(filename):
            raise OSError('File {} does not exists'.format(filename))
        config_yaml = None
        try:
            with open(filename) as fileio_wrapper:
                config_yaml = yaml.safe_load(fileio_wrapper)
        except yaml.scanner.ScannerError:
            message = 'Some error with file format in {} (should be YAML)'\
                .format(filename)
            raise OSError(message)
        if not config_yaml or 'config' not in config_yaml:
            message = 'Config {} is empty, or have not "config" block'\
                .format(filename)
            raise OSError(message)
        return cls(config_yaml['config'])
