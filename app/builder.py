"""Abstact builder"""
import abc
import six


@six.add_metaclass(abc.ABCMeta)
class DnsBuilder(object):
    """DnsBuilder Abstact class"""

    @abc.abstractmethod
    def add_record(self, record):
        """add record to builder"""
        raise NotImplementedError

    @abc.abstractmethod
    def add_alias(self, alias_record):
        """add alias to builder"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_result(self):
        """return builded product"""
        raise NotImplementedError
