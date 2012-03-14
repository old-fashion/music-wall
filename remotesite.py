import os
import time
import logging
import re

from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch
from google.appengine.api import taskqueue

class RemoteSite():

    def extract(self, url):
        data = "URL: " + url
        result = urlfetch.fetch(url)
        content = ""

        if result.status_code == 200:
            content = result.content.decode('utf-8')
      
        MUSIC_PARSER = r'href="(?P<music>.+(mp3|MP3))">'
        mlist = []
        for m in re.finditer(MUSIC_PARSER, content):
            item = url + m.group('music')
            data += item + '\n'
            mlist.append(item)

        taskqueue.add(queue_name='funnel', url='/funnel', \
                      params={'site': url, 'type': 'nginx'})

        return data

    def html(self, url):
        result = "<html><body><pre>"
        result += self.extract(url)
        result += "</pre></body></html>"
        return result

    def testhtml(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'template/sitetest.html')
        result = template.render(path, template_values)
        return result

    def put(self, metadata):
        pass

remotesite = RemoteSite()

if __name__ == "__main__":
    remotetag = RemoteTag()
    #remotetag.extract("file://1.mp3")
    #result = remotetag.extract("http://127.0.0.1/1.mp3")
    result = remotetag.extract("http://blackout.lgnas.com:9000/disk/volume1/Multimedia/Music/OST/Vicky%20Cristina%20Barcelona%20%282008%29/01%20Barcelona.mp3")
    print result
