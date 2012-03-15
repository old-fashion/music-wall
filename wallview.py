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
    MENU = [
        # id, name, style, (x,y,width,height)
        ('mcloud', 'CONNECT\nTO\nCLOUD', 'background:rgba(240,0,0,1);', (0, 0, 4, 1)),
        ('malbum', 'ALBUM', 'background:rgba(160,114,163,1);', (1, 0, 1, 3)),
        ('martist', 'ARTIST', 'background:rgba(203,191,143,1);', (2, 0, 3, 3)),
        ('myear', 'YEAR', 'background:rgba(241,223,63,1);', (3, 0, 3, 3)),
        ('mgenre', 'GENRE', 'background:rgba(217,214,207,1);', (0, 1, 3, 3)),
        ('mrating', 'RATING', 'background:rgba(74,106,163,1);', (1, 1, 3, 3)),
        ('mrandom', 'RANDOM', 'background:rgba(226,193,214,1);', (2, 1, 3, 3)),
        ('mhowto', 'HOT TO', 'background:rgba(77,77,77,1);', (3, 1, 3, 3)),
        ('mnone', 'NONE', 'background:rgba(188,48,83,1);', (0, 2, 3, 3)),
    ]
    MBOX_X = 4
    MBOX_Y = 3
    MBOX_WIDTH = 160
    MBOX_HEIGHT = 160
    MBOX_X_MARGIN = 24
    MBOX_Y_MARGIN = 14
    menus = []

    def __init__(self):

        unit_width = self.MBOX_WIDTH + self.MBOX_X_MARGIN
        unit_height = self.MBOX_HEIGHT + self.MBOX_Y_MARGIN

        self.javascript = "mbox = {\n"
        for id, name, style, location in self.MENU:
            x, y, width, height = location
            x_org = - unit_width * self.MBOX_X / 2 + x * unit_width
            y_org = - unit_height * self.MBOX_Y / 2 + y * unit_height
            x_target = self.MBOX_WIDTH * width + (width - 1) * self.MBOX_X_MARGIN
            y_target = self.MBOX_HEIGHT * height + (height - 1) * self.MBOX_Y_MARGIN
            style += "margin-left:{}px; margin-top:{}px;".format(x_org, y_org)
            self.menus.append((id, name, style, "aa"))

            margin_top = 0
            margin_left = 0
            if y + height > self.MBOX_Y:
                margin_top = ((self.MBOX_Y - y) - height) * unit_height
            if x + width > self.MBOX_X:
                margin_left = ((self.MBOX_X - x) - width) * unit_width

            self.javascript += "  '{}': {{\n".format(id)
            self.javascript += "    'margin-top': {},\n".format(margin_top)
            self.javascript += "    'margin-left': {},\n".format(margin_left)
            self.javascript += "    'width': {},\n".format(x_target)
            self.javascript += "    'height': {},\n".format(y_target)
            self.javascript += "  },\n"
        self.javascript += "};\n"

    def html(self, preset='pc'):
        if preset not in self.PRESET:
            preset = 'pc'
        model = wallmodel.get(*self.PRESET.get(preset))

        template_values = {
            'menus': self.menus,
            'boxes': model,
            'border': 2,
            'javascript': self.javascript,
        }
        path = os.path.join(os.path.dirname(__file__), 'template/wallview.html')
        result = template.render(path, template_values)
        return result

wallview = WallView()

if __name__ == "__main__":
    pass
