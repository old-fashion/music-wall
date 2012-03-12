from google.appengine.ext import db

class MusicModel(db.Model):
    uid = db.StringProperty(required=True, indexed=True)

    title = db.StringProperty()
    artist = db.StringProperty()
    album = db.StringProperty()

    #cover = db.BlobProperty()

