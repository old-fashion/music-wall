# -*- coding: utf-8 -*-
import re
import webapp2
import logging

from google.appengine.ext import db

from musicmodel import *

class CoverHandler(webapp2.RequestHandler):
    def get(self):
        url = self.request.get('url')
        logging.info(url)
        #music = cover.get(url)
        #logging.info(str(music))
        query = MusicModel.all()
        query.filter('url =', url)
        result = query.fetch(limit=1)

        self.response.headers['Content-Type'] = 'image/jpeg'   
        if len(result) > 0 and result[0].cover:
            self.response.out.write(result[0].cover_data)
    
class Cover():
    def get(self, url):
        result = db.GqlQuery("SELECT cover FROM MusicModel WHERE url = :1 LIMIT 1",
                    url).fetch(1)
        if len(result) > 0 and result.cover_data:
            return result[0]
        else:
            return None

cover = Cover()

"""
from BeautifulSoup import BeautifulSoup


class MyOpener(urllib.FancyURLopener):  
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'  

class CoverHandler(webapp2.RequestHandler):
    def image_addr(self, word, idx):  
        offset = 0

        urllib._urlopener = MyOpener()  
        f = urllib.urlopen('http://images.google.com/images?hl=ko&source=hp&q='+word+
                           '&btnG=%EC%9D%B4%EB%AF%B8%EC%A7%80+%EA%B2%80%EC%83%89&gbv=2&aq=f&oq=&'+
                           'tbs=isz:ex,iszw:300,iszh:300,ift:jpg')  

        soup = BeautifulSoup(f.read())
        image_table = soup.find(id='ires')
        images = image_table.findAll('td')

        idx %= len(images)

        for image in images:
            try:
                if idx == offset:
                    pattern = re.compile('imgurl=(.*?\.(jpg|JPG))')
                    return pattern.search(str(image)).group(1)
                else:
                    offset += 1
            except:
               return 'http://goo.gl/yBF0N' #warning page

    def get(self):
        word = "bluenote"
        idx = 0
        self.response.headers['Content-Type'] = 'image/jpeg'
        self.response.headers['Content-Disposition'] = 'attachment; filename=%s%s.jpg' % (word, idx)
        self.redirect(self.image_addr(word, int(idx)))
"""
