"""Module with Database fetcher methods"""
import _mysql_exceptions


class DataFetcher(object):
    """fetcher data from db and return it, also store connectin options"""

    def __init__(self, connection, is_inner_dns=True):
        self.connection = connection
        self.is_inner_dns = is_inner_dns
        self._last_state = None
        self._data = None

    def is_fetch_success(self):
        """return state of last host request"""
        return self._last_state

    def get_data(self):
        """return data from last host request"""
        return self._data

    def get_hosts(self):
        """get active hosts from db with ip addresses"""
        ip_field = 'inIP' if self.is_inner_dns else 'outIP'
        fields = 'name, {} as address'.format(ip_field)
        query = "SELECT {} from hosts where status = 1".format(fields)
        self._execute(query)

    def get_domains(self):
        """get active domain by hosts db with"""
        hostname = 'backup' if self.is_inner_dns else 'moscow'
        query = 'SELECT url, host, dns_servers as tag from aliases ' \
                'where dns_servers in ("both", "{}")'.format(hostname)
        self._execute(query)

    def _execute(self, query_string):
        try:
            self._last_state = True
            self._data = self.connection.query(query_string, [])
        except _mysql_exceptions.MySQLError:
            self._last_state = False
            self._data = ()
