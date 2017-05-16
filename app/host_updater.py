"""Module with HostUpdater class"""
import json
import os

from app.formatter import Formatter


class ZoneNotFoundException(Exception):
    """Zone Not Found Exception"""
    pass


class HostUpdater(object):
    """Class allow update host by zone"""

    def __init__(self, fetcher, dns_dir, zones, cache_dir):
        self.fetcher = fetcher
        self.dns_dir = dns_dir
        self.zones = zones
        self.cache_dir = cache_dir
        self.hosts = []

    @property
    def cache_file(self):
        """return cache file"""
        return os.path.join(self.cache_dir, 'hosts.cache')

    @property
    def temp_cache_file(self):
        """return temp cache file"""
        return self.cache_file + '.temp'

    def refresh_cache(self):
        """Refresh cache file"""
        self.fetcher.get_hosts()
        if self.fetcher.is_fetch_success():
            self.hosts = self.fetcher.get_data()
            if os.path.exists(self.cache_file):
                return self._update_cache_file()
            return self._create_cache_file()
        elif os.path.exists(self.cache_file):
            with open(self.cache_file) as fhandler:
                self.hosts = json.loads(fhandler.read())
        else:
            self.hosts = []

    def update_zones(self):
        """Update hosts in all zones"""
        for zone in self.zones:
            self.update_zone(zone)

    def update_zone(self, zone):
        """Update hosts only in certain zone"""
        if zone not in self.zones:
            raise ZoneNotFoundException('zone "{}" not found'.format(zone))

        zone_file = os.path.join(self.dns_dir, zone + '.hosts')
        lines = []
        lines.append(['$ORIGIN', zone + '.'])
        lines.append([])

        self.refresh_cache()

        for host in self.hosts:
            name = host['name'].split('.')[0]
            address = host['address']
            lines.append([name, 'IN', 'A', address])

        with open(zone_file, 'w+') as filehandler:
            filehandler.write(Formatter.sort_by_column(lines))

    def _update_cache_file(self):
        """Private: update cache file if it really need"""
        try:
            if os.path.exists(self.temp_cache_file):
                os.remove(self.temp_cache_file)
            self._write_json_file(self.temp_cache_file)
            if self._diff_files():
                os.remove(self.cache_file)
                os.rename(self.temp_cache_file, self.cache_file)
                return True
            os.remove(self.temp_cache_file)
        except OSError:
            pass
        return False

    def _diff_files(self):
        """Private: return true if files differ"""
        file_one = self.cache_file
        file_two = self.temp_cache_file
        with open(file_one) as fhandler_one:
            file_one_content = fhandler_one.read()
        with open(file_two) as fhandler_two:
            file_two_content = fhandler_two.read()
        return bool(file_one_content != file_two_content)

    def _create_cache_file(self):
        """Update file with new data"""
        try:
            self._write_json_file(self.cache_file)
            return True
        except OSError:
            return False

    def _write_json_file(self, filename):
        """Write current data to file"""
        with open(filename, 'w+') as filehandler:
            filehandler.write(self._get_formatted_data())

    def _get_formatted_data(self):
        """Return json data"""
        return json.dumps(self.hosts, indent=4)
