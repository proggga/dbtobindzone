"""Module with HostUpdater class"""
from app.updaters.updater import Updater


class HostUpdater(Updater):
    """Class allow update host by zone"""

    def __init__(self, *args, **kwargs):
        super(HostUpdater, self).__init__(*args, **kwargs)
        self.data = []
        self.prefix = 'hosts'

    def _format_zone_file_content(self, zone_name, initial_lines=None):
        """Method which format file content"""
        lines = list(initial_lines)
        for host in self.data:
            name = host['name'].split('.')[0]
            address = host['address']
            lines.append([name, 'IN', 'A', address])
        return lines
