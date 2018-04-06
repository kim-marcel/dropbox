from google.appengine.ext import ndb


class File(ndb.Model):
    # Name of the file as string
    name = ndb.StringProperty()

    # Data of the file
    blob = ndb.BlobKeyProperty()
