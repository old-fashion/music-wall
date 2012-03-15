import os
import time
import logging

from musicmodel import *
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

from google.appengine.ext.webapp import template

class RemoteTag():
    def html(self, url):
        result = "<html><body><pre>"
        result += extract(url)
        result += "</pre></body></html>"
        return result

    def testhtml(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'template/tagtest.html')
        result = template.render(path, template_values)
        return result

def extract(url):
    logging.info(url)
    starttime = time.time()

    # 1. Extract metadata from URL
    music = MP3(url, ID3=EasyID3)
    result = music.pprint()
    cover = music.tags['cover_data']
    
    model = MusicModel(url=url)
    for item in music.tags:
        setattr(model, item, music.tags[item][0])
    model.put()
   
    return result

remotetag = RemoteTag()

if __name__ == "__main__":
    remotetag = RemoteTag()
    #remotetag.extract("file://1.mp3")
    #result = remotetag.extract("http://127.0.0.1/1.mp3")
    result = remotetag.extract("http://127.0.0.1:9000/disk/volume1/Multimedia/Music/OST/Vicky%20Cristina%20Barcelona%20%282008%29/01%20Barcelona.mp3")
    print result
