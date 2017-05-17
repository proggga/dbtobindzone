"""Module with Database fetcher methods"""
from _mysql_exceptions import MySQLError


class DataFetcher(object):
    """fetcher data from db and return it, also store connectin options"""

    def __init__(self, connection):
        self.connection = connection
        self._last_state = None
        self._data = None

    def is_fetch_success(self):
        """return state of last host request"""
        return self._last_state

    def get_data(self):
        """return data from last host request"""
        return self._data

    def execute(self):
        """get query and execute"""
        self._execute(self.get_query())

    def get_query(self):
        """Return query for next executing"""
        raise NotImplementedError("You should implement this in your subclass")

    def _execute(self, query_string):
        try:
            self._last_state = True
            self._data = self.connection.query(query_string, [])
        except MySQLError:
            self._last_state = False
            self._data = ()
