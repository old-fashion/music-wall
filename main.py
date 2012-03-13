#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import webapp2
import cgi

from wallmodel import wallmodel
from wallview import wallview
from remotetag import remotetag
from remotesite import remotesite

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('Hello world!')

class ViewHandler(webapp2.RequestHandler):
    def get(self, preset='tv'):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(wallview.html(preset))

class TagHandler(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(remotetag.html(cgi.escape(self.request.get('url'))))

class TagTestHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(remotetag.testhtml())

class SiteHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(remotesite.html(cgi.escape(self.request.get('url'))))

class SiteTestHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(remotesite.testhtml())


app = webapp2.WSGIApplication([
    ('/', MainHandler), 
    (r'/view', ViewHandler),
    (r'/view/(\w+)', ViewHandler),
    (r'/tag', TagHandler),
    (r'/tagtest', TagTestHandler),
    (r'/site', SiteHandler),
    (r'/sitetest', SiteTestHandler),
], debug=True)

