"""Module with exceptions."""


class DbDnsException(Exception):
    """Exception of module."""


class ZoneException(DbDnsException):
    """Common zone exception."""


class ZoneNotFoundException(ZoneException):
    """Zone Not Found Exception."""


class InvalidZone(ZoneException):
    """Invalid zone name/path."""


class DnsRecordException(DbDnsException):
    """Common DnsRecord exception."""


class DnsRecordNotFound(DnsRecordException):
    """DnsRecord not found."""


class ReferenceToNoneException(DnsRecordException):
    """Reference to empty target."""


class InvalidReferencesException(DnsRecordException):
    """Reference is not valid (not str or list)."""
