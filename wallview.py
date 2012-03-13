import logging
import string
import os
import random

from google.appengine.api import urlfetch
from google.appengine.ext import db
from google.appengine.ext.webapp import template

from wallmodel import wallmodel

class WallView():
    PRESET = {
        #'NAME': [width, height, one_unit_size, unit_max, border],
        'tv': [1280, 700, 80, 3, 2],
        'pc': [1920, 1080, 80, 3, 2],
    }

    def html(self, preset='pc'):
        if preset not in self.PRESET:
            preset = 'pc'
        model = wallmodel.get(*self.PRESET.get(preset))

        template_values = {
            'boxes': model,
            'border': 2,
        }
        path = os.path.join(os.path.dirname(__file__), 'template/wallview.html')
        result = template.render(path, template_values)
        return result

wallview = WallView()

if __name__ == "__main__":
    pass
