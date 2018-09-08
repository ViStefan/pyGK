#!/usr/bin/python3

from ngkapi import loadComments

# terminal escape codes for colors and styles
HEADER = '\033[95m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
BOLD = '\033[1m'
ENDC = '\033[0m'

# filenames
LAST_SEEN_FILE = 'last_seen'
BLACKLIST_FILE = 'blacklist'

def esc(e, s):
    return '{}{}{}'.format(e, s, ENDC)

def readLastSeen():
    try:
        return int(open(LAST_SEEN_FILE, 'r').read())
    except:
        return loadComments()[-1]['id']

def writeLastSeen(last):
    open(LAST_SEEN_FILE, 'w').write(str(last))

def readBlackList():
    try:
        return [x.rstrip('\n') for x in open(BLACKLIST_FILE, 'r').readlines()]
    except:
        return []

def commentUrl(comment):
    return "http://govnokod.ru/{}#comment{}".format(comment['post_id'], comment['id'])

def userUrl(comment):
    return "http://govnokod.ru/user/{}".format(comment['user_id'])
