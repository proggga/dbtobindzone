"""Updater common data"""
import abc
import json
import os

from app.exceptions import ZoneNotFoundException
from app.file_helper import FileHelper
from app.formatter import Formatter


class Updater(object):
    """Class allow update host by zone"""

    def __init__(self, fetcher, dns_dir, zones, cache_dir):
        self.fetcher = fetcher
        self.dns_dir = dns_dir
        self.zones = zones
        self.cache_dir = cache_dir
        self.prefix = 'updater'
        self.data = []

    def refresh_cache(self):
        """Refresh cache file"""
        self.fetcher.execute()
        if self.fetcher.is_fetch_success():
            self.data = self.fetcher.get_data()
            if os.path.exists(self.cache_file):
                return self._update_cache_file()
            return self._create_cache_file()
        elif os.path.exists(self.cache_file):
            with open(self.cache_file) as fhandler:
                self.data = json.loads(fhandler.read())
        else:
            self.data = []

    @property
    def cache_file(self):
        """return cache file"""
        return os.path.join(self.cache_dir, self.prefix + '.cache')

    @property
    def temp_cache_file(self):
        """return temp cache file"""
        return self.cache_file + '.temp'

    def update_zones(self):
        """Update hosts in all zones"""
        for zone in self.zones:
            self.update_zone(zone)

    @abc.abstractmethod
    def _format_zone_file_content(self, zone_name,
                                  initial_lines=None):  # pragma: no cover
        """Format data for file"""
        pass

    def update_zone(self, zone):
        """Update hosts only in certain zone"""
        if zone not in self.zones:
            raise ZoneNotFoundException('zone "{}" not found'.format(zone))

        self.refresh_cache()
        initial_lines = [
            ['$ORIGIN', zone + '.'],
            []
        ]
        lines = self._format_zone_file_content(zone,
                                               initial_lines=initial_lines)
        zone_file = self.get_zone_file(zone)
        with open(zone_file, 'w+') as filehandler:
            filehandler.write(Formatter.sort_by_column(lines))

    def get_zone_file(self, zone):
        """Get Zone file"""
        return os.path.join(self.dns_dir, zone + '.' + self.prefix)

    def _update_cache_file(self):
        """Private: update cache file if it really need"""
        try:
            if os.path.exists(self.temp_cache_file):
                os.remove(self.temp_cache_file)
            self._write_json_file(self.temp_cache_file)
            if self.files_differ():
                os.remove(self.cache_file)
                os.rename(self.temp_cache_file, self.cache_file)
                return True
            os.remove(self.temp_cache_file)
        except EnvironmentError:
            pass
        return False

    def files_differ(self):
        """return true if files differ"""
        return FileHelper.differ(self.cache_file, self.temp_cache_file)

    def _create_cache_file(self):
        """Update file with new data"""
        try:
            self._write_json_file(self.cache_file)
            return True
        except EnvironmentError:
            return False

    def _write_json_file(self, filename):
        """Write current data to file"""
        with open(filename, 'w+') as filehandler:
            filehandler.write(self._get_formatted_data())

    def _get_formatted_data(self):
        """Return json data"""
        return json.dumps(self.data, indent=4)
