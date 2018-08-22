#!/usr/bin/python3

from ngkapi import loadFreshComments as load, loadComments
from core import *

TAB = '  '  # two spaces 

def buildTree(comments):
    tree = {}
    for comment in reversed(comments):
        tree[comment['id']] = [comment, []]
        if comment['parent_id'] in tree:
            tree[comment['parent_id']][1].append(comment['id'])
    return tree


def byPosts(tree, blacklist):
    posts = {}
    counters = {} 
    for node in tree:
        post_id = tree[node][0]['post_id']
        if post_id in posts:
            posts[post_id][node] = tree[node]
            if tree[node][0]['user_name'] in blacklist:
                counters[post_id][1] += 1
            else:
                counters[post_id][0] += 1
        else:
            posts[post_id] = {node: tree[node]}
            if tree[node][0]['user_name'] in blacklist:
                counters[post_id] = [0, 1]
            else:
                counters[post_id] = [1, 0]

    return (counters, posts)

def recursivePrint(tree, node, blacklist, depth = 0):
    new = tree[node][0]
    nick = new['user_name']
    nick = esc(WARNING, nick) if nick in blacklist else nick
    print('{}{}'.format(TAB * depth, nick), end='')
    if depth == 0:
        url = ': http://govnokod.ru/{}#comment{}'.format(new['post_id'], new['id'])
        if new['user_name'] in blacklist:
            print(esc(WARNING, url))
        else:
            print(url)
    else:
        print()
    children = tree[node][1]
    del tree[node]
    for child in children:
        recursivePrint(tree, child, blacklist, depth + 1)

def printFresh(last_seen):
    new = load(last_seen)
    if len(new):
        last_seen = new[0]['id']
    blacklist = readBlackList()
    counters, new = byPosts(buildTree(new), blacklist)
    for post in sorted(list(new)): 
        tree = new[post]
        print('{}'.format(
            esc(BOLD, '{}: {} {}'.format(
                esc(HEADER, '#{}'.format(post)),
                esc(OKGREEN, '+{}'.format(counters[post][0])),
                esc(WARNING, '+{}'.format(counters[post][1]))
            ))
        ))
        while len(new[post]) > 0: 
            recursivePrint(new[post], sorted(list(new[post]))[0], blacklist)
        print()
    return last_seen

writeLastSeen(printFresh(readLastSeen()))
