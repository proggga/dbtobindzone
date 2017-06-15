"""Main application."""
from app.fetcher.host_data_fetcher import HostDataFetcher
from app.misc.dot_config import DotConfig
from app.misc.sql import SqlConnection
from app.updaters.domain_updater import DomainUpdater
from app.updaters.host_updater import HostUpdater


class DBtoDns(object):
    """Entry point of updater."""

    def __init__(self, config_path):
        """Init connection and fetchers from config."""
        config = DotConfig.load(config_path)
        self.connection = SqlConnection(**config.connection)
        host_fetcher = HostDataFetcher(self.connection,
                                       **config.database_hosts)
        self.host_updater = HostUpdater(fetcher=host_fetcher,
                                        dns_dir=config.dnspath,
                                        zones=config.zones,
                                        cache_dir=config.zone_cache_dir)
        domain_fetcher = HostDataFetcher(self.connection,
                                         **config.database_hosts)
        self.domain_updater = DomainUpdater(fetcher=domain_fetcher,
                                            dns_dir=config.dnspath,
                                            zones=config.zones,
                                            cache_dir=config.zone_cache_dir)

    def update(self):
        """Update any."""
        self.update_hosts()
        self.update_domains()

    def update_hosts(self):
        """Update hosts."""
        self.host_updater.refresh_cache()
        print("Hosts:", self.host_updater.data)

    def update_domains(self):
        """Update domains."""
        self.domain_updater.refresh_cache()
        print("Domains:", self.domain_updater.data)
