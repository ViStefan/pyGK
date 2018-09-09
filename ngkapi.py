#!/usr/bin/python3

import requests
import json
from core import GK_URL

class Comment():
    def __init__(self, comment):
        self.__dict__.update(comment)
        self.url = '{}{}#comments{}'.format(GK_URL, self.post_id, self.id)
        self.user_url = '{}user/{}'.format(GK_URL, self.user_id)

class NGK:
    # captain obvious comment
    NGK_URL = 'http://b.gcode.cx/ngk/api/'

    def __init__(self, core):
        self.core = core

    # returns 20 last comments or comments elder than before
    # `before` should be like '2018-03-06T19:59:21Z'
    def loadComments(self, before = None):
        url = '{}comments'.format(self.NGK_URL)
        if before is not None:
            url += '?before={}'.format(before)

        r = requests.get(url) 
        if r.status_code == 200:
            return r.json()
        else:
            raise Exception('Error getting data from ngk api')

    # returns all the comments newer than last_seen in config
    def refresh(self):
        last_seen = self.core.config.getint('main', 'last_seen')
        comments = self.loadComments() 
        recent = comments[-1]['id']
        while recent > last_seen:
            comments += self.loadComments(comments[-1]['posted'])
            recent = comments[-1]['id']

        return [Comment(c) for c in comments[:recent - last_seen - 1]]
