"""Abstact builder"""
import abc
import six


@six.add_metaclass(abc.ABCMeta)
class DnsBuilder(object):
    """DnsBuilder Abstact class"""

    @abc.abstractmethod
    def add_record(self, record):  # pragma: no cover
        """add record to builder"""
        pass

    @abc.abstractmethod
    def add_alias(self, alias_record):  # pragma: no cover
        """add alias to builder"""
        pass

    @abc.abstractmethod
    def get_result(self):  # pragma: no cover
        """return builded product"""
        pass
