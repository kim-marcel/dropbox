from google.appengine.ext import ndb


class MyUser(ndb.Model):
    # Object of anagrams where all the anagrams of the user are stored
    name = ndb.StringProperty()
