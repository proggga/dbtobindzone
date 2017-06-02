"""DnsRecord State"""
from app.misc.exceptions import ReferenceToNoneException


class DnsRecordState(object):
    """DnsRecordState it is state of DnsRecord"""

    _instance = None

    @classmethod
    def get_name(cls):
        """Rerturn status name"""
        return cls.__name__

    def __new__(cls):
        if not cls._instance:
            inst = super(DnsRecordState, cls).__new__(cls)
            cls._instance = inst
        return cls._instance

    @staticmethod
    def get_string(record):
        """used by DnsRecord as __str__ method"""
        raise NotImplementedError()

    @staticmethod
    def add_references(record, new_references):
        """used by DnsRecord as add references method"""
        raise NotImplementedError()


class AliasDnsRecordState(DnsRecordState):
    """AliasDnsRecordState it is state of DnsRecord"""

    @staticmethod
    def get_string(record):
        if not record.references_to:
            raise ReferenceToNoneException()
        return "{} IN CNAME {}".format(record.domain_name,
                                       record.references_to.domain_name)

    @staticmethod
    def add_references(record, new_references):
        """Add references to alias not implemented"""
        pass


class BalancedHostDnsRecordState(DnsRecordState):
    """BalancedHostDnsRecordState it is state of DnsRecord"""

    @staticmethod
    def get_string(record):
        """Return __str__ content"""
        if not record.references_to:
            raise ReferenceToNoneException()
        result = []
        for reference in record.references_to:
            result.append("{} IN A {}".format(record.domain_name,
                                              reference))
        return '\n'.join(result)

    @staticmethod
    def add_references(record, new_references):
        "add new reference to"
        if new_references not in record.references_to:
            record.references_to.append(new_references)


class HostDnsRecordState(DnsRecordState):
    """HostDnsRecordState it is state of DnsRecord"""

    @staticmethod
    def get_string(record):
        """Return __str__ content"""
        if not record.references_to:
            raise ReferenceToNoneException()
        return "{} IN A {}".format(record.domain_name,
                                   record.references_to)

    @staticmethod
    def add_references(record, new_references):
        "add new reference to, switch state"
        last_address = record.references_to
        record.references_to = [last_address, new_references]
        record.change_state(BalancedHostDnsRecordState())
