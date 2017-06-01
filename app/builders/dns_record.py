"""Dns Record"""
from app.misc.exceptions import DnsRecordNotFound
from app.misc.exceptions import ReferenceToNoneException


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
        self.references_to = references_to

    def get_zone_file(self):
        """Get format for zone and childs"""
        result = []
        if str(self):
            result.append(str(self))
        for alias in self.aliases.values():
            if isinstance(alias, DnsRecord):
                result.extend(alias.get_zone_file())
            else:
                if alias != '':
                    result.append(alias)
        return result

    def search(self, domain_name):
        """Search domain_name in aliases"""
        if self.fqdn == domain_name:
            return self
        if domain_name in self.aliases:
            return self.aliases[domain_name]
        for alias in self.aliases.values():
            search_result = alias.search(domain_name)
            if search_result:
                return search_result
        raise DnsRecordNotFound

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

    def get_references(self):
        """get references object"""
        if isinstance(self.references_to, str):
            return self.references_to
        return self.references_to.domain_name

    def get_type(self):
        """get references object"""
        if isinstance(self.references_to, str):
            return "A"
        return "CNAME"

    def __str__(self):
        if not self.references_to:
            raise ReferenceToNoneException()
        return "{} IN {} {}".format(self.domain_name,
                                    self.get_type(),
                                    self.get_references())
