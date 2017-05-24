"""Module with exceptions"""


class ZoneException(Exception):
    """Common zone exception"""
    pass


class ZoneNotFoundException(ZoneException):
    """Zone Not Found Exception"""
    pass


class InvalidZone(ZoneException):
    """Invalid zone name/path"""
    pass
