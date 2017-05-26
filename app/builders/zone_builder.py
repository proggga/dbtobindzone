"""Abstact builder"""
import re

from app.builders.builder import DnsBuilder
from app.misc.dot_config import DotConfig
from app.misc.exceptions import InvalidZone
from app.misc.formatter import Formatter


class ZoneBuilder(DnsBuilder):
    """Zone file builder"""

    def __init__(self, zone_name, *args, **kwargs):
        super(ZoneBuilder, self).__init__(*args, **kwargs)
        ZoneBuilder.check_zone(zone_name)
        self.zone = zone_name
        self._data = []
        self._hosts = {}
        self._append_header()

    def _append_header(self):
        self._data.append('$ORIGIN {}.'.format(self.zone))

    def add_record(self, record):
        """add record to builder"""
        new_record = DotConfig(record)
        dns_line = "{} IN A {}".format(new_record.hostname,
                                       new_record.address)

        if new_record.hostname not in self._hosts:
            self._hosts[new_record.hostname] = []

        if new_record.address not in self._hosts[new_record.hostname]:
            self._hosts[new_record.hostname].append(new_record.address)
            self._data.append(dns_line)

    def add_alias(self, alias_record):
        """add alias to builder"""
        new_record = DotConfig(alias_record)
        if new_record.address not in self._hosts:
            if re.match(r".*{}(\.?)$".format(self.zone), new_record.address):
                address = new_record.address.replace('.' + self.zone + '.',
                                                     '')
                address = address.replace('.' + self.zone,
                                          '')
                if address in self._hosts:
                    new_record.address = address
                elif not new_record.address.endswith('.'):
                    new_record.address += '.'

            dns_line = "{} IN CNAME {}".format(new_record.hostname,
                                               new_record.address)
            self._data.append(dns_line)

    def get_result(self):
        """return builded product"""
        return Formatter.sort_str_by_column('\n'.join(self._data))

    def flush_result(self):
        """Method for clearing builder data"""
        self._data = []
        self._append_header()

    @staticmethod
    def check_zone(zone_name):
        """Check zone for valid (thx for regex StackOverFlow)"""
        if (not re.match(r'^(((?!-))(xn--)?[a-z0-9][a-z0-9-_]'
                         r'{0,61}[a-z0-9]{0,1}\.)?(x--)'
                         r'?([a-z0-9][a-z0-9\-]{0,60}[a-z0-9]|'
                         r'[a-z0-9][a-z0-9-]{0,29}[a-z0-9]'
                         r'\.[a-z]{2,})\.?$',
                         zone_name)):
            raise InvalidZone('Zone {} is not valid'.format(zone_name))
