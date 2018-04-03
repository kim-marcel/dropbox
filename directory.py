from google.appengine.ext import ndb


class Directory(ndb.Model):
    # The key of the directory in which this one is in
    # Used to move up, is empty, when in root directory
    parent_directory = ndb.KeyProperty()
    # Keys of all the files in this directory
    files = ndb.KeyProperty(repeated=True)
    # name
    name = ndb.StringProperty()
    # path
    path = ndb.StringProperty()
    # all sub directories in this directory
    directories = ndb.KeyProperty(repeated=True)
