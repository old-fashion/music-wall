from google.appengine.ext import db

class MusicModel(db.Model):
    url = db.LinkProperty(required=True, indexed=True)
    size = db.IntegerProperty()

    title = db.StringProperty()
    artist = db.StringProperty()
    album = db.StringProperty()
    year = db.StringProperty()
    genre = db.StringProperty()
    track = db.StringProperty()
    cover = db.BlobProperty()

    playcount = db.IntegerProperty()
    playdate = db.DateTimeProperty()
