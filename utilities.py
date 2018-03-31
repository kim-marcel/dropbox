from google.appengine.ext import ndb
from google.appengine.api import users
from myuser import MyUser
from directory import Directory
import logging
import re  # regex


# Get user from this page
def get_user():
    return users.get_current_user()


# get user from data
def get_my_user():
    user = get_user()
    if user:
        my_user_key = ndb.Key(MyUser, user.user_id())
        return my_user_key.get()


def user_is_logged_in():
    return True if get_user() else False


# returns true if for this user a myuser object already exists in the datastore
def user_exists():
    return True if get_my_user() else False


def add_new_user(user):
    my_user = MyUser(id=user.user_id())
    my_user.put()
    add_new_directory(None, None, my_user)


def add_new_directory(name, parent_directory, my_user):
    if parent_directory is None:
        # the root-directory is being created
        id = my_user.key.id() + '/'
    else:
        # a regular directory gets created
        id = parent_directory + '/' + name

    directory = Directory(id=id)
    directory.parent_directory = parent_directory
    directory.put()

    my_user.directories.append(directory.key)
    my_user.put()


def get_login_url(main_page):
    return users.create_login_url(main_page.request.uri)


def get_logout_url(main_page):
    return users.create_logout_url(main_page.request.uri)
