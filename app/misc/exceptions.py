"""Module with exceptions"""


class DbDnsException(Exception):
    """Exception of module"""
    pass


class ZoneException(DbDnsException):
    """Common zone exception"""
    pass


class ZoneNotFoundException(ZoneException):
    """Zone Not Found Exception"""
    pass


class InvalidZone(ZoneException):
    """Invalid zone name/path"""
    pass


class DnsRecordException(DbDnsException):
    """Common DnsRecord exception"""
    pass


class DnsRecordNotFound(DnsRecordException):
    """DnsRecord not found"""
    pass


class ReferenceToNoneException(DnsRecordException):
    """Reference to empty target"""
    pass
