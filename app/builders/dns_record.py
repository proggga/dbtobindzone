"""Dns Record"""
from app.misc.exceptions import DnsRecordNotFound
from app.misc.exceptions import InvalidReferencesException

from app.builders.dns_state import AliasDnsRecordState
from app.builders.dns_state import BalancedHostDnsRecordState
from app.builders.dns_state import HostDnsRecordState


class DnsRecord(object):
    """Dns record class"""

    def __init__(self, zone, domain_name, references_to):
        if zone.startswith('.'):
            zone = zone[1:]
        if domain_name.endswith(zone):
            domain_name = domain_name.replace('.' + zone, '')
        self.domain_name = domain_name
        self.zone = zone
        self.aliases = {}
        self.state = None
        self.set_references(references_to)

    def set_references(self, new_references):
        """Set state to self"""
        self.references_to = new_references
        if isinstance(new_references, list):
            self.change_state(BalancedHostDnsRecordState())
        elif isinstance(new_references, DnsRecord):
            self.change_state(AliasDnsRecordState())
        elif isinstance(new_references, str):
            self.change_state(HostDnsRecordState())
        else:
            raise InvalidReferencesException

    def add_references(self, new_references):
        """add another references_to"""
        self.state.add_references(self, new_references)

    def change_state(self, new_state):
        """Change DnsRecordState"""
        self.state = new_state

    def get_zone_file(self):
        """Get format for zone and childs"""
        result = []
        result_line = str(self)
        if result_line:
            result.append(result_line)
        for alias in self.aliases.values():
            result.extend(alias.get_zone_file())
        return result

    def search(self, domain_name):
        """Search domain_name in aliases"""
        if self._domain_is_mine(domain_name):
            return self
        if domain_name in self.aliases:
            return self.aliases[domain_name]
        for alias in self.aliases.values():
            search_result = alias.search(domain_name)
            if search_result:
                return search_result
        raise DnsRecordNotFound

    def _domain_is_mine(self, domain_name):
        return (self.fqdn == domain_name or
                domain_name == self.domain_name)

    def add_alias(self, alias_domain_name):
        """Add alias method"""
        alias = DnsRecord(self.zone, alias_domain_name, self)
        if alias.fqdn not in self.aliases:
            self.aliases[alias.fqdn] = alias
        return alias

    def add_subdomain(self, subdomain):
        """Add subdomain as alias method"""
        alias = DnsRecord(self.zone, subdomain + '.' + self.domain_name, self)
        if alias.fqdn not in self.aliases:
            self.aliases[alias.fqdn] = alias
        return alias

    @property
    def fqdn(self):
        """Return fqdn"""
        return '.'.join((self.domain_name, self.zone))

    def __str__(self):
        return self.state.get_string(self)
