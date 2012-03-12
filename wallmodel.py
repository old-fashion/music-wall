import logging
import string
import random

class WallModel():
    SAMPLE_URL = 'http://images.bol.de/images-adb/79/66/7966a83c-22bf-4c5c-83cd-17ef7b264d9a.jpg'
    SAMPLE_URL2 = "http://storage.canalblog.com/81/33/500408/29407917.jpg"
    COVER_URL = "http://twnoti.appspot.com/400x400/tralfaz-archives%20"

    cache = {}
    MAX_CACHE_SIZE = 5

    def wall(self, width, height, unit, unit_max, border=2):
        result = []
        unitx = width / unit + 4
        unity = height / unit + 4
        pindex = 0
        tiles = self.tile(unitx, unity, unit_max)
        for x, y, size in tiles:
            box = {}
            box['id'] = 'box_' + str(pindex)
            box['top'] = y * unit - int(unit * 1.5)
            box['left'] = x * unit - int(unit * 1.5)
            box['width'] = unit * size - border
            box['height'] = unit * size - border
            box['url'] = self.COVER_URL \
                + random.choice(string.ascii_lowercase) \
                + random.choice(string.ascii_lowercase) \
                + '/' + str(pindex % 40)
            pindex += 1
            box['url'] = self.SAMPLE_URL2
            result.append(box)

        return result

    def get(self, width, height, unit, unit_max, border=2):
        key = "{}.{}.{}.{}.{}".format(width, height, unit, unit_max, border);
        if key not in self.cache:
            self.cache[key] = []
        if len(self.cache[key]) < self.MAX_CACHE_SIZE:
            result = self.wall(width, height, unit, unit_max, border)
            self.cache[key].append(result)
            logging.info("New Wall added")
        else:
            result = random.choice(self.cache[key])
            logging.info("Use old Wall")

        return result
    
    def tile_fill(self, canvas, x, y, size, char):
        for tile in canvas[y:y+size]:
            tile[x:x+size] = [char] * size

    def tile_available(self, canvas, x, y, size):
        if canvas[y][x] != '_':
            return 0

        for target in xrange(2, size + 1):
            if x + target - 1 >= len(canvas[0]) or y + target - 1 >= len(canvas):
                return target - 1
            for i in xrange(target):
                if canvas[y+i][x+target-1] != '_' or canvas[y+target-1][x+i] != '_':
                    return target - 1
        return size

    def tile(self, width, height, max_size):
        canvas = [['_'] * width for i in range(height)]  
        boxes = []
        count = 0;
        recent_size = 0;

        for y in xrange(height):
            for x in xrange(width):
                avail = self.tile_available(canvas, x, y, max_size)
                if avail != 0:
                    size = random.choice(range(1, avail + 1))
                    if size == recent_size:
                        size = random.choice(range(1, avail + 1))
                    self.tile_fill(canvas, x, y, size, str(count))
                    boxes.append((x, y, size))
                    count += 1 
                    recent_size = size
        return boxes

    def tile_pprint(self, canvas):
        for tile in canvas:
            print tile

wallmodel = WallModel()

