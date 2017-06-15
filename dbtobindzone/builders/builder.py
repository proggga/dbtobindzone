"""Abstact builder."""
import abc
import six


@six.add_metaclass(abc.ABCMeta)
class DnsBuilder(object):
    """DnsBuilder Abstact class."""

    @abc.abstractmethod
    def add_record(self, record):  # pragma: no cover
        """Add record to builder."""
        pass

    @abc.abstractmethod
    def add_alias(self, alias_record):  # pragma: no cover
        """Add alias to builder."""
        pass

    @abc.abstractmethod
    def get_result(self):  # pragma: no cover
        """Return builded product."""
        pass
