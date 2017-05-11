#!/usr/bin/env python
'''gen new hosts'''
from app.application import App
from app.dot_config import DotConfig


if __name__ == '__main__':
    try:
        CONFIG = DotConfig.load('config.yml')
        APP = App(CONFIG)
        APP.update_hosts()
        APP.update_kodwebs()
    except Exception as ex:
        print("An uknown exceptions was raised {}".format(str(ex)))
        exit(2)
