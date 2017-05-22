"""Module with DomainUpdater class"""
from app.updaters.updater import Updater


class DomainUpdater(Updater):
    """Class allow update host by zone"""

    def __init__(self, *args, **kwargs):
        super(DomainUpdater, self).__init__(*args, **kwargs)
        self.data = []
        self.prefix = 'domains'

    def _format_zone_file_content(self, zone_name):
        """Method which format file content"""
        self.set_zone_header(zone_name)
        lines = self.get_initial_lines()
        for domain in self.data:
            name = domain['url']
            if name.endswith(zone_name):
                address = domain['host'].split('.')[0]
                lines.append([name, 'IN', 'CNAME', address])
        return lines
