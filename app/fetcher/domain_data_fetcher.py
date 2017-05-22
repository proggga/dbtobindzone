"""Module with Database fetcher methods"""
from app.fetcher.data_fetcher import DataFetcher


class DomainDataFetcher(DataFetcher):
    """fetcher data from db and return it, also store connectin options"""

    def __init__(self, connection, tags, **kwargs):
        super(DomainDataFetcher, self).__init__(connection)
        self.tags = tags
        self.url_field = kwargs.get('url_field', 'url')
        self.common_tag = kwargs.get('common_tag', 'any')
        self.hostname_field = kwargs.get('hostname_field', 'host')
        self.tag_field = kwargs.get('tag_field', 'tag')
        self.domain_table = kwargs.get('domain_table', 'urls')

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
