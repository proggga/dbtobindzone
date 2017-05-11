"""Module with HostUpdater class"""
import json
import os

from app.formatter import Formatter


class ZoneNotFoundException(Exception):
    pass


class HostUpdater(object):
    """Class allow update host by zone"""

    def __init__(self, fetcher, dns_dir, zones, cache_dir):
        self.fetcher = fetcher
        self.dns_dir = dns_dir
        self.zones = zones
        self.cache_dir = cache_dir
        self.cache_file = os.path.join(self.cache_dir, 'hosts.cache')
        self.temp_cache_file = os.path.join(self.cache_dir,
                                            'hosts.cache') + '.temp'
        self.hosts = []

    def refresh_cache(self):
        """Refresh cache file"""
        self.fetcher.get_hosts()
        if self.fetcher.last_fetch_status_ok():
            self.hosts = self.fetcher.get_data()
            if os.path.exists(self.cache_file):
                return self._update_cache_file()
            return self._create_cache_file()
        return False

    def update(self):
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

        if not os.path.exists(self.cache_file):
            self.refresh_cache()

        with open(self.cache_file) as fhandler:
            data = json.loads(fhandler.read())
        for host in data:
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
                if os.path.exists(self.cache_file):
                    os.remove(self.cache_file)
                os.rename(self.temp_cache_file, self.cache_file)
                return True
            else:
                os.remove(self.temp_cache_file)
                return False
        except OSError as ex:
            print(str(ex))
            return False

    def _diff_files(self):
        """Private: return true if files differ"""
        file_one = self.cache_file
        file_two = self.temp_cache_file
        with open(file_one) as fhandler:
            file_one_content = fhandler.read()
        with open(file_two) as fhandler:
            file_two_content = fhandler.read()
        return bool(file_one_content != file_two_content)

    def _create_cache_file(self):
        """Update file with new data"""
        try:
            self._write_json_file(self.cache_file)
            return True
        except OSError as ex:
            print(str(ex))
            return False

    def _write_json_file(self, filename):
        """Write current data to file"""
        with open(filename, 'w+') as filehandler:
            filehandler.write(self._get_formatted_data())

    def _get_formatted_data(self):
        """Return json data"""
        return json.dumps(self.hosts, indent=4)
