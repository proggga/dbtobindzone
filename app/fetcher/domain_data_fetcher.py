"""Module with Database fetcher methods"""
from app.fetcher.data_fetcher import DataFetcher


class DomainDataFetcher(DataFetcher):
    """fetcher data from db and return it, also store connectin options"""

    def __init__(self, connection, tags, common_tag='any',
                 domain_table='urls',
                 url_field='url', hostname_field='host',
                 tag_field='tag'):
        super(DomainDataFetcher, self).__init__(connection)
        self.tags = tags
        self.url_field = url_field
        self.common_tag = common_tag
        self.hostname_field = hostname_field
        self.tag_field = tag_field
        self.domain_table = domain_table

    def get_query(self):
        """get active domain by hosts db with"""
        return ('SELECT {} as url, {} as host, {} as tag from {} as urls {}'
                .format(self.url_field,
                        self.hostname_field,
                        self.tag_field,
                        self.domain_table,
                        self._format_tags_where()))


    def _format_tags_where(self):
        if not self.tags:
            return ""

        result = '%" or tag like "%'.join(self.tags)
        if result:
            result = 'where (tag like "%{}%")'.format(result)
        return result
