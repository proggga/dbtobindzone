"""Module allow load yaml config to object, accessed by dot

Allow create yaml config and load, easy access to childs and data by dots
like Example:
config = DotConfig.load('filename')
config.key.list # item1, item2
"""
# coding: utf-8
import os
import yaml


class DotConfig(object):
    """Config object accessed by dots"""

    def __init__(self, configration):
        if not isinstance(configration, dict):
            raise TypeError("Config should be "
                            "a Dictionary not {}"
                            .format(configration.__class__))
        self._cfg = configration

    def __getattr__(self, key):
        """Get from config new DotConfig (if dict) or return by value"""
        data = self._cfg[key]
        if isinstance(data, dict):
            return DotConfig(data)
        return data

    def __str__(self):
        return str(self._cfg)

    def keys(self):
        """return keys of inner dict"""
        return self._cfg.keys()

    def __getitem__(self, item):
        return self._cfg.__getitem__(item)

    @classmethod
    def load(cls, filename):
        """load file from yaml and return loaded DotConfig"""

        if not os.path.exists(filename):
            raise OSError('File {} does not exists'.format(filename))
        config_yaml = None
        try:
            with open(filename) as fileio_wrapper:
                config_yaml = yaml.safe_load(fileio_wrapper)
        except yaml.scanner.ScannerError:
            message = ('Some error with file format in {} (should be YAML)'
                       .format(filename))
            raise OSError(message)

        key = 'config'
        message = ('Config {} is empty or have not "{}" block'
                   .format(filename, key))
        return DotConfig._return_or_rise(key, config_yaml, message)

    @classmethod
    def _return_or_rise(cls, key, data_dict, message='Error in dict'):
        if data_dict and key in data_dict:
            return cls(data_dict[key])
        else:
            raise OSError(message)
