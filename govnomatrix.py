#!/usr/bin/python3

from matrix_client.client import MatrixClient
from bs4 import BeautifulSoup as bs
import re

class Govnomatrix:
    def __init__(self, core):
        server = core.config.get('matrix', 'server')
        username = core.config.get('matrix', 'username')
        password = core.config.get('matrix', 'password')
        room = core.config.get('matrix', 'room')

        self.client = MatrixClient(server)
        self.client.login_with_password(username=username, password=password)
        self.room = self.client.join_room(room)

    # returns special url if there is corresponding user in room
    # same for recipient
    # if possible, url points to matrix user, otherwise to GK profile
    def getUserUrl(self, c, recipient=False):
        username = c.recipient.lower() if recipient else c.user_name.lower()
        url = c.recipient_url if recipient else c.user_url

        for user in self.room.get_joined_members():
            if user.get_display_name().lower() == username:
                return 'https://matrix.to/#/{}'.format(user.user_id)

        return url 

    def prepareHtml(self, c):
        text = []
        for line in c.text.split('\n'):
            plain = bs(line, "lxml").text
            if len(plain) and plain[0] == '>':
                text.append('<blockquote>{}</blockquote>'.format(line.replace('&gt;', '', 1)))
            else:
                text.append(line)

        soup = bs(''.join(text), "lxml")
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
        
        return re.sub(r'(</pre>|</blockquote>|</h1>|<br/>)<br/>', r'\1', str(soup))

    def template(self, c):
        if c.recipient:
            if c.recipient.lower() == c.user_name.lower():
                recipient = 'added'
            else:
                recipient = 'to <a href="{}">{}</a>'.format(
                    self.getUserUrl(c, recipient=True),
                    c.recipient
                )
        else:
            recipient = 'into {}'.format(c.post_id)

        return """
<a href="{}"><b>{}</b></a> {} <a href="{}"><b>#</b></a>:<br/>
{}
""".format(
        self.getUserUrl(c),
        c.user_name,
        recipient,
        c.url,
        self.prepareHtml(c))

    def send(self, c):
        self.room.send_html(self.template(c))
