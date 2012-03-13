import os
import time
import logging

from musicmodel import *
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

from google.appengine.ext.webapp import template

class RemoteTag():
    def extract(self, url):
        starttime = time.time()
        audio = MP3(url, ID3=EasyID3)
        result = audio.pprint()
        result += "\n\nElapsed Time : {}".format(time.time() - starttime)
        logging.info(url)

        """
        audio = MP3(url)
        cover = audio.tags['APIC:'].data
        with open('cover.jpg', 'wb') as img:
            img.write(cover)

        print "Elapsed Time : {}".format(time.time() - starttime)
        """
        return result

    def html(self, url):
        result = "<html><body><pre>"
        result += self.extract(url)
        result += "</pre></body></html>"
        return result

    def testhtml(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'template/tagtest.html')
        result = template.render(path, template_values)
        return result

    def put(self, metadata):
        pass

remotetag = RemoteTag()

if __name__ == "__main__":
    remotetag = RemoteTag()
    #remotetag.extract("file://1.mp3")
    #result = remotetag.extract("http://127.0.0.1/1.mp3")
    result = remotetag.extract("http://blackout.lgnas.com:9000/disk/volume1/Multimedia/Music/OST/Vicky%20Cristina%20Barcelona%20%282008%29/01%20Barcelona.mp3")
    print result
