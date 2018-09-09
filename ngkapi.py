#!/usr/bin/python3

import requests
import json
from core import GK_URL

class Comment():
    def __init__(self, comment):
        self.__dict__.update(comment)
        # urls to be inserted in different representations
        self.url = '{}{}#comments{}'.format(GK_URL, self.post_id, self.id)
        self.user_url = '{}user/{}'.format(GK_URL, self.user_id)
        self.recipient = None

    def set_recipient(self, r):
        self.recipient = r['user_name']
        self.recipient_url = '{}user/{}'.format(GK_URL, r['user_id'])

class NGK:
    # captain obvious comment
    NGK_URL = 'http://b.gcode.cx/ngk/api/'

    def __init__(self, core):
        self.core = core


    def get(self, method, params=None):
        url = '{}{}'.format(self.NGK_URL, method)
        r = requests.get(url, params=params)
        return r.json()

    # returns 20 last comments or comments elder than before
    # `before` should be like '2018-03-06T19:59:21Z'
    def comments(self, before = None):
        return self.get('comments', {'before': before})

    # returns all comments of post with specified id
    def post(self, id):
        return self.get('post/{}'.format(id))['comments']

    # loads parent comment of each comment in comments
    # and fills comment fields about what it replies to
    def load_recipient(self, comments):
        posts = {}
        for c in comments:
            if c.parent_id:
                if c.post_id not in posts:
                    posts[c.post_id] = self.post(c.post_id)
                c.set_recipient([r for r in posts[c.post_id] if r['id'] == c.parent_id][0])

    # returns all the comments newer than last_seen in config
    def refresh(self):
        last_seen = self.core.config.getint('main', 'last_seen')
        comments = self.comments() 
        recent = comments[-1]['id']
        while recent > last_seen:
            comments += self.comments(comments[-1]['posted'])
            recent = comments[-1]['id']

        comments = [Comment(c) for c in comments[:recent - last_seen - 1]]

        if self.core.config.getboolean('ngk', 'load_recipient'):
            self.load_recipient(comments)    

        return comments
