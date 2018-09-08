#!/usr/bin/python3

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

from ngkapi import loadFreshComments as load, loadComments
from core import *
import time
from bs4 import BeautifulSoup as bs 

from govnomatrix import Govnomatrix

def init(gm = None):
    stock = loadComments()
    printComments(stock, readBlackList(), gm)
    return stock[0]['id']

def pretty(text):
    return bs(text, "html.parser").text

def printComment(c):
    print('{} into #{} | {}\n{}'.format(
        esc(BOLD, c['user_name']),
        c['post_id'],
        commentUrl(c),
        pretty(c['text'])
    ))
    print()

def printComments(comments, blacklist, gm = None):
    for comment in reversed(comments):
        if not comment['user_name'] in blacklist:
            printComment(comment)
            if gm:
                gm.send(comment)

def refresh(last, gm = None):
    stock = load(last)
    printComments(stock, readBlackList(), gm)
    return last if len(stock) == 0 else stock[0]['id']

gm = Govnomatrix()
last = init(gm)
while True:
    last = refresh(last, gm)
    time.sleep(10)
