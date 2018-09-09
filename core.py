#!/usr/bin/python3

import configparser

GK_URL = 'http://govnokod.ru/'

class Core:
    def __init__(self):
        self.read_config()

    def read_config(self):
        self.config = configparser.RawConfigParser()
        self.config.read('pyGK.cfg')
        self.blacklist = self.config.get('main', 'blacklist').split(' ')

    def write_config(self):
        with open('pyGK.cfg', 'w') as config:
            self.config.write(config)
