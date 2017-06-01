"""Dns Record"""


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
        domain = self.domain_name
        fqdn_data = [domain]
        if isinstance(self.references_to, str):
            fqdn_data.append(self.zone)
        else:
            fqdn_data.append(self.zone)
            # elif not domain.endswith(self.references_to.fqdn):
            #     fqdn_data.append(self.references_to.fqdn)

        return '.'.join(fqdn_data)

    @property
    def server_name(self):
        """Get full name without zone"""
        return self.fqdn.replace('.' + self.zone, '')

    def get_references(self):
        """get references object"""
        if isinstance(self.references_to, str):
            return self.references_to
        return self.references_to.server_name

    def get_type(self):
        """get references object"""
        if isinstance(self.references_to, str):
            return "A"
        return "CNAME"

    def __str__(self):
        return "{} IN {} {}".format(self.server_name,
                                    self.get_type(),
                                    self.get_references())
