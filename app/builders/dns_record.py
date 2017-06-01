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
        self.references_to = references_to

    def add_alias(self):
        """Add alias method"""
        pass

    @property
    def fqdn(self):
        """Return fqdn"""
        domain = self.domain_name
        fqdn_data = [domain]
        if isinstance(self.references_to, str):
            fqdn_data.append(self.zone)
        else:
            if domain.endswith(self.references_to.domain_name):
                fqdn_data.append(self.zone)
            elif not domain.endswith(self.references_to.fqdn):
                fqdn_data.append(self.references_to.fqdn)

        return '.'.join(fqdn_data)

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
        return "{} IN {} {}".format(self.domain_name,
                                    self.get_type(),
                                    self.get_references())
