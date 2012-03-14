import os
import time
import logging
import re
import webapp2

from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch
from google.appengine.api import taskqueue

class FunnelHandler(webapp2.RequestHandler):
    def post(self):
        url = self.request.get('site')
        type = self.request.get('type')

        if type == 'nginx':
            funnel = NginxFunnel(url)
            funnel.list()
            funnel.process()

class Funnel():
    def name(self):
        return 'funnel'

class NginxFunnel(Funnel):
    def __init__(self, url):
        self.url = url
        self.mlist = []

    def list(self):
        logging.info(self.url)
        result = urlfetch.fetch(self.url)
        content = ""

        if result.status_code == 200:
            content = result.content.decode('utf-8')

        MUSIC_PARSER = r'href="(?P<music>.+(mp3|MP3))">'
        for m in re.finditer(MUSIC_PARSER, content):
            item = self.url + m.group('music')
            self.mlist.append(item)

    def process(self):
        for item in self.mlist:
            time.sleep(1)
            logging.info(str(item))

if __name__ == "__main__":
    pass
