from google.appengine.ext import db

class MusicModel(db.Model):
    url = db.LinkProperty(required=True, indexed=True)
    size = db.IntegerProperty()

    title = db.StringProperty()
    artist = db.StringProperty()
    album = db.StringProperty()
    date = db.StringProperty()
    genre = db.StringProperty(indexed=True)
    discnumber = db.StringProperty()
    tracknumber = db.StringProperty()
    cover = db.BooleanProperty()
    cover_data = db.BlobProperty(default=None)

    playcount = db.IntegerProperty()
    playdate = db.DateTimeProperty()
