from google.appengine.ext import ndb


class MyUser(ndb.Model):
    # The current path in which the user is in/ was in the last time
    current_directory = ndb.KeyProperty()
    # A repeated KeyProperty in which every directory will be stored in
    directories = ndb.KeyProperty(repeated=True)
    # A KeyProperty which stores the root directory key
    root_directory = ndb.KeyProperty()
