"""Module with Database fetcher methods."""
from dbtobindzone.fetcher.data_fetcher import DataFetcher


class HostDataFetcher(DataFetcher):
    """fetcher data from db by hosts."""

    def __init__(self, connection, table='hosts', ip_field='ip',
                 hostname_field='hostname'):
        """Init default."""
        super(HostDataFetcher, self).__init__(connection)
        self.table = table
        self.ip_field = ip_field
        self.hostname_field = hostname_field

    def get_query(self):
        """Get query of hosts."""
        return ("SELECT {} as hostname, {} as address "
                "from {} where status = 1"
                .format(self.hostname_field,
                        self.ip_field,
                        self.table))
