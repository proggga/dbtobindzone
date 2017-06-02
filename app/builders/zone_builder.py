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

        self._records = {}
        self._aliases_without_ref = {}

    def add_record(self, record):
        """add record to builder"""
        new_record = DotConfig(record)

        fqdn = new_record.hostname + '.' + self.zone
        domain_name = new_record.hostname
        address = new_record.address
        if fqdn not in self._records:
            self._records[fqdn] = DnsRecord(self.zone,
                                            domain_name,
                                            address)
            if fqdn in self._aliases_without_ref:
                alias = self._aliases_without_ref[fqdn]
                del self._aliases_without_ref[fqdn]
                self._records[fqdn].add_alias(alias.domain_name)

        else:
            self._records[fqdn].add_references(address)

    def add_alias(self, alias_record):
        """add alias to builder"""
        new_record = DotConfig(alias_record)
        name = new_record.hostname
        refs = new_record.address
        if refs not in self._records:
            result = self._search_record(refs)
            if result:
                result.add_alias(name)
            if not result and name not in self._records:
                alias = DnsRecord(self.zone, name,
                                  DnsRecord(self.zone, refs, ''))
                self._aliases_without_ref[refs] = alias
        else:
            self._records[refs].add_alias(new_record.hostname)

    def _search_record(self, refs):
        for record in self._records:
            try:
                result_record = record.search(refs)
            except DnsRecordNotFound:
                pass
            else:
                return result_record

    def get_result(self):
        """return builded product"""
        result = '$ORIGIN {}.\n'.format(self.zone)
        for record in self._records.values():
            result += '\n'.join(record.get_zone_file())

        for alias in self._aliases_without_ref.values():
            result += '\n'.join(alias.get_zone_file())

        return Formatter.sort_str_by_column(result)

    def flush_result(self):
        """Method for clearing builder data"""
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
