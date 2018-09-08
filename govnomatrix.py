#!/usr/bin/python3

from matrix_client.client import MatrixClient
from core import userUrl, commentUrl
from bs4 import BeautifulSoup as bs

class Govnomatrix:
    def __init__(self):
        self.client = MatrixClient('http://matrix.org')
        self.client.login_with_password(username='govnomatrix', password='bormandmylove')
        self.room = self.client.join_room('#testgkbotroom:matrix.org')

    def getUserUrl(self, comment):
        for user in self.room.get_joined_members():
            if user.get_display_name().lower() == comment['user_name'].lower():
                return 'https://matrix.to/#/{}'.format(user.user_id)
            else:
                return userUrl(comment) 

    def prepareHtml(self, comment):
        soup = bs(comment['text'])
        for tag in soup.find_all():
            if tag.name == 'code':
                tag['class'] = 'language-{}'.format(tag['class'][0])
            elif tag.name == 'span':
                if tag['style'] == 'text-decoration:underline;':
                    tag.name = 'u'
                elif tag['style'] == 'text-decoration:line-through;':
                    tag.name = 'strike'
                elif tag['style'][:5] == 'color':
                    tag.name = 'font'
                    tag['color'] = tag['style'][6:-1]
                elif tag['style'] == 'font-size:20px;':
                    tag.name = 'h1'
                
                del tag['style']
        
        return soup

    def send(self, c):
        self.room.send_html("""<a href="{}"><b>{}</b></a> в {} <a href="{}"><b>#</b></a>:<br>
{}""".format(self.getUserUrl(c), c['user_name'], c['post_id'], commentUrl(c), self.prepareHtml(c)))
