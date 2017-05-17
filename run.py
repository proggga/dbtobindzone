#!/usr/bin/env python
"""gen new hosts"""
from app.db_to_dns import DBtoDns

if __name__ == '__main__':
    DNS_WRITER = DBtoDns('config.yml')
    DNS_WRITER.update_hosts()
