"""Abstact builder"""
import re

from app.builders.builder import DnsBuilder
from app.builders.dns_record import DnsRecord
from app.misc.dot_config import DotConfig
from app.misc.exceptions import DnsRecordNotFound
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

        self._records = {}
        self._aliases = {}

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

        fqdn = new_record.hostname + '.' + self.zone
        domain_name = new_record.hostname
        if fqdn not in self._records:
            self._records[fqdn] = DnsRecord(self.zone,
                                            domain_name,
                                            new_record.address)

    def add_alias(self, alias_record):
        """add alias to builder"""
        new_record = DotConfig(alias_record)
        name = new_record.hostname
        refs = new_record.address
        if refs not in self._records:
            found = False
            for record in self._records:
                try:
                    result_record = record.search(refs)
                except DnsRecordNotFound:
                    pass
                else:
                    found = True
                    result_record.add_alias(name)
            if not found and name not in self._records:
                self._aliases[name] = DnsRecord(self.zone,
                                                name,
                                                DnsRecord(self.zone,
                                                          refs,
                                                          ''))
        else:
            self._records[refs].add_alias(new_record.hostname)
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
        # return Formatter.sort_str_by_column('\n'.join(self._data))
        result = '$ORIGIN {}.\n'.format(self.zone)
        for record in self._records.values():
            result += '\n'.join(record.get_zone_file())

        for alias in self._aliases.values():
            result += '\n'.join(alias.get_zone_file())

        return Formatter.sort_str_by_column(result)

    def flush_result(self):
        """Method for clearing builder data"""
        self._data = []
        self._append_header()

        keys = list(self._records.keys())
        for key in keys:
            del self._records[key]
        del self._records
        self._records = {}

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
