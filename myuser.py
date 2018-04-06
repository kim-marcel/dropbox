from google.appengine.ext import ndb


class MyUser(ndb.Model):
    # A KeyProperty which stores the root directory key
    root_directory = ndb.KeyProperty()

    # The current path in which the user is in/ was in the last time
    current_directory = ndb.KeyProperty()
