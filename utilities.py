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
        directory_id = my_user.key.id() + '/'

        directory = Directory(id=directory_id)
        directory.parent_directory = parent_directory
        directory.name = 'root'
        directory.path = '/'
        directory.put()

        my_user.root_directory = directory.key
        my_user.put()
    else:
        # a regular directory gets created
        if is_in_root_directory(my_user):
            directory_id = parent_directory + name
        else:
            directory_id = parent_directory + '/' + name

        parent_directory = ndb.Key(Directory, my_user.key.id() + parent_directory)
        logging.debug(parent_directory)

        directory = Directory(id=directory_id)

        # check if directory already exists
        if directory.key not in my_user.directories:
            parent_directory = get_current_directory(my_user).get()
            parent_directory.directories.append(directory.key)
            parent_directory.put()

            directory.parent_directory = parent_directory.key
            directory.name = name
            if is_in_root_directory(my_user):
                directory.path = parent_directory.path + name
            else:
                directory.path = parent_directory.path + '/' + name
            directory.put()

            my_user.directories.append(directory.key)
            my_user.put()


# returns true if current directory is root directory
def is_in_root_directory(my_user):
    current_directory = get_current_directory(my_user).get()
    return True if current_directory.parent_directory is None else False


# returns key of current directory
def get_current_directory(my_user):
    return my_user.current_directory


# returns key of parent directory
def get_parent_directory(my_user):
    current_directory = get_current_directory(my_user)
    return current_directory.get().parent_directory


def get_login_url(main_page):
    return users.create_login_url(main_page.request.uri)


def get_logout_url(main_page):
    return users.create_logout_url(main_page.request.uri)
