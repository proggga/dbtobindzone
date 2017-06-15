"""Module with DomainUpdater class."""
from app.updaters.updater import Updater


class DomainUpdater(Updater):
    """Class allow update host by zone."""

    def __init__(self, *args, **kwargs):
        """Init default."""
        super(DomainUpdater, self).__init__(*args, **kwargs)
        self.data = []
        self.prefix = 'domains'

    def _format_zone_file_content(self, zone_name, initial_lines=None):
        """Format file content."""
        lines = list(initial_lines)
        for domain in self.data:
            name = domain['url']
            if name.endswith(zone_name):
                address = domain['host'].split('.')[0]
                lines.append([name, 'IN', 'CNAME', address])
        return lines
