#!/usr/bin/python3

import requests
import json
from core import GK_URL

class Comment:
    def __init__(self, comment):
        self.__dict__.update(comment)
        # urls to be inserted in different representations
        self.url = '{}{}#comment{}'.format(GK_URL, self.post_id, self.id)
        self.user_url = '{}user/{}'.format(GK_URL, self.user_id)

        self.recipient = None

    def set_recipient(self, user_name, user_id):
        self.recipient = user_name
        self.recipient_url = '{}user/{}'.format(GK_URL, user_id)

class NGK:
    NGK_URL = 'http://b.gcode.cx/ngk/api/'

    def __init__(self, use_recipients):
        self.use_recipients = use_recipients
        self.seen = [] 
        self.top = None 
        self.refresh()

    # request to API
    def get(self, method, params=None):
        url = '{}{}'.format(self.NGK_URL, method)
        try:
            r = requests.get(url, params=params)
            return r.json()
        except:
            raise Exception("Can't send request to {}".format(NGK_URL))

    # returns 20 last comments or comments elder than before
    # `before` should be like '2018-03-06T19:59:21Z'
    def comments(self, before = None):
        return self.get('comments', {'before': before})

    # returns all comments of post with specified id
    def post(self, id, params):
        return self.get('post/{}'.format(id))['comments']

    # loads parent comment of each comment in comments
    # and fills comment fields about what it replies to
    def load_recipients(self, comments):
        for c in comments:
            if c.parent_id:
                r = self.get('comments', {'id': c.parent_id})[0]
            else:
                r = self.get('post/{}'.format(c.post_id), {'no_comments': True})
            c.set_recipient(r['user_name'], r['user_id'])


    # returns new comments 
    def refresh(self):
        # get all comments, appeared in API after last visit
        comments = self.comments() 
        top = self.top if self.top else comments[0]['posted']
        bottom = comments[-1]['posted']
        while top <= bottom:
            comments += self.comments(bottom)
            bottom = comments[-1]['posted']

        self.top = comments[0]['posted']

        # find unseen comments among them
        new = []
        for c in comments:
            if c['id'] not in self.seen:
                self.seen.append(c['id'])
                new.append(Comment(c))
                
        # load replyTo information if needed
        if self.use_recipients:
            self.load_recipients(new)

        return new 
