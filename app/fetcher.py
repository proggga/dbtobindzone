'''
Module with Database fetcher methods
'''


class DataFetcher(object):
    '''fetcher data from db and return it, also store connectin options'''

    def __init__(self, connection, is_inner_dns=True):
        self.connection = connection
        self.is_inner_dns = is_inner_dns
        self._last_state = None
        self._data = None

    def last_fetch_status_ok(self):
        '''return state of last host request'''
        return self._last_state

    def get_data(self):
        '''return data from last host request'''
        return self._data

    def get_hosts(self):
        '''get active hosts from db with ip addresses'''

        ip_field = 'inIP' if self.is_inner_dns else 'outIP'
        fields = 'name, {} as address'.format(ip_field)
        query_string = "SELECT {} from hosts where status = 1".format(fields)
        try:
            self._last_state = True
            self._data = self.connection.query(query_string, [])
        except Exception:
            self._last_state = False
            self._data = ()
