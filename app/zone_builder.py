"""Abstact builder"""
import re
from app.builder import DnsBuilder
from app.exceptions import InvalidZone
# from app.dot_config import DotConfig


class ZoneBuilder(DnsBuilder):
    """Zone file builder"""

    def __init__(self, zone_name, *args, **kwargs):
        super(ZoneBuilder, self).__init__(*args, **kwargs)
        ZoneBuilder.check_zone(zone_name)
        self.zone = zone_name
        self._data = []
        self._hosts = {}

    def add_record(self, record):
        """add record to builder"""
        # data = DotConfig(record)

    def add_alias(self, alias_record):
        """add alias to builder"""
        pass

    def get_result(self):
        """return builded product"""
        return '\n'.join(self._data)

    @staticmethod
    def check_zone(zone_name):
        """Check zone for valid (thx for regex StackOverFlow)"""
        if (not re.match(r'^(((?!-))(xn--)?[a-z0-9][a-z0-9-_]'
                         r'{0,61}[a-z0-9]{0,1}\.)?(x--)'
                         r'?([a-z0-9\-]{1,61}|[a-z0-9-]{1,30}'
                         r'\.[a-z]{2,})\.?$',
                         zone_name)):
            raise InvalidZone('Zone {} is not valid'.format(zone_name))
