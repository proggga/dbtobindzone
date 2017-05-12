"""Main application"""
from app.data_fetcher import DataFetcher
from app.host_updater import HostUpdater
from app.sql import SqlConnection
from app.dot_config import DotConfig


class DBtoDns(object):
    """Entry point of updater"""

    def __init__(self, config_path):
        config = DotConfig.load(config_path)
        self.connection = SqlConnection(**config.connection)
        self.fetcher = DataFetcher(self.connection, config.dns.is_inner)
        self.host_updater = HostUpdater(fetcher=self.fetcher,
                                        dns_dir=config.dns.path,
                                        zones=config.zones,
                                        cache_dir=config.zone_cache_dir)

    def update_hosts(self):
        """main method"""
        print("Status is ", self.host_updater.refresh_cache())
        self.host_updater.update()

    def update_kodwebs(self):
        """main method"""
        print("Status is ", self.host_updater.refresh_cache())
        self.host_updater.update()
