#!/usr/bin/python3

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
from bs4 import BeautifulSoup as bs 
import time

from core import Core 
from ngkapi import NGK 
from govnomatrix import Govnomatrix

def print_comment(c):
    print('{} into #{} | {}\n{}'.format(
        c.user_name,
        c.post_id,
        c.url,
        bs(c.text, "html.parser").text
    ))
    print()

def process(comments):
    for c in reversed(comments):
        if not c.user_name in core.blacklist:
            print_comment(c) 
            if gm:
                gm.send(c)

core = Core()
ngk = NGK(core)
gm = Govnomatrix(core) if core.config.getboolean('matrix', 'enabled') else None

while True:
    try:
        stock = ngk.refresh()
        if len(stock):
            core.config.set('main', 'last_seen', stock[0].id)
            core.write_config()

        process(stock)
    except:
        pass
        
    time.sleep(10)
