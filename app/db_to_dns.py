"""Main application"""
from app.fetcher.host_data_fetcher import HostDataFetcher
from app.dot_config import DotConfig
from app.host_updater import HostUpdater
from app.domain_updater import DomainUpdater
from app.sql import SqlConnection


class DBtoDns(object):
    """Entry point of updater"""

    def __init__(self, config_path):
        config = DotConfig.load(config_path)
        self.connection = SqlConnection(**config.connection)
        host_fetcher = HostDataFetcher(self.connection,
                                       **config.database_hosts)
        self.host_updater = HostUpdater(fetcher=host_fetcher,
                                        dns_dir=config.dns.path,
                                        zones=config.zones,
                                        cache_dir=config.zone_cache_dir)
        domain_fetcher = HostDataFetcher(self.connection,
                                         **config.database_hosts)
        self.domain_updater = DomainUpdater(fetcher=domain_fetcher,
                                            dns_dir=config.dns.path,
                                            zones=config.zones,
                                            cache_dir=config.zone_cache_dir)

    def update_hosts(self):
        """main method"""
        self.host_updater.refresh_cache()
        self.domain_updater.refresh_cache()
        print(self.host_updater.hosts)
        print(self.domain_updater.hosts)
