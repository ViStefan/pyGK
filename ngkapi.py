#!/usr/bin/python3
import requests
import json 

# captain obvious comment
NGK_URL = 'http://b.gcode.cx/ngk/api'

# returns 20 last comments or comments elder then [before]
# [before] should be like '2018-03-06T19:59:21Z'
def loadComments(before = None):
    url = '{}/comments'.format(NGK_URL)
    if before is not None:
        url += '?before={}'.format(before)

    r = requests.get(url) 
    if r.status_code == 200:
        return r.json()
    else:
        raise Exception('Error getting data from ngk api')

# returns all the comments newer then [last_seen]
# [last_seen]: id of comment (int)
def loadFreshComments(last_seen):
    comments = loadComments() 
    recent = comments[-1]['id']
    while recent > last_seen:
        comments += loadComments(comments[-1]['posted'])
        recent = comments[-1]['id']

    return comments[:-last_seen + recent - 1]
