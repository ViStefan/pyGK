#!/usr/bin/python3

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

from ngkapi import loadFreshComments as load, loadComments
from core import *
import time
from bs4 import BeautifulSoup as bs 

def init():
    stock = loadComments()
    printComments(stock, readBlackList())
    return stock[0]['id']

def pretty(text):
    return bs(text, "html.parser").text

def printComment(c):
    print('{} into #{} | {}\n{}'.format(
        esc(BOLD, c['user_name']),
        c['post_id'],
        'http://govnokod.ru/{}#comment{}'.format(
            c['post_id'],
            c['id']
        ),
        pretty(c['text'])
    ))
    print()

def printComments(comments, blacklist):
    for comment in reversed(comments): 
        if not comment['user_name'] in blacklist:
            printComment(comment)

def refresh(last):
    stock = load(last)
    printComments(stock, readBlackList())
    return last if len(stock) == 0 else stock[0]['id']

last = init()
while True:
    try:
        last = refresh(last)
    except:
        pass
    time.sleep(10)
