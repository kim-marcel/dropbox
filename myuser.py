from google.appengine.ext import ndb


class MyUser(ndb.Model):
    # The current path in which the user is in/ was in the last time
    current_patch = ndb.StringProperty()
    # A repeated KeyProperty in which every directory will be stored in
    directories = ndb.KeyProperty(repeated=True)
