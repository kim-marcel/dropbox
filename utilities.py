from google.appengine.ext import ndb
from google.appengine.api import users
from myuser import MyUser
from directory import Directory
from file import File
from google.appengine.ext import blobstore
import logging


# Get user from this page
def get_user():
    return users.get_current_user()


# get user from data
def get_my_user():
    user = get_user()
    if user:
        my_user_key = ndb.Key(MyUser, user.user_id())
        return my_user_key.get()


def get_directories_in_current_path(my_user):
    return get_current_directory_key(my_user).get().directories


def get_files_in_current_path(my_user):
    return get_current_directory_key(my_user).get().files


def user_is_logged_in():
    return True if get_user() else False


# returns true if for this user a myuser object already exists in the datastore
def user_exists():
    return True if get_my_user() else False


def add_new_user(user):
    my_user = MyUser(id=user.user_id())
    add_new_directory(None, None, my_user)
    # set current path on first login to root directory
    my_user.current_directory = ndb.Key(Directory, my_user.key.id() + '/')
    my_user.put()


def add_new_directory(name, parent_directory, my_user):
    if parent_directory is None:
        # the root-directory is being created
        add_root_directory(my_user)
    else:
        # a regular directory gets created
        add_directory(name, parent_directory, my_user)


def add_root_directory(my_user):
    directory_id = my_user.key.id() + '/'
    directory = Directory(id=directory_id)

    directory.parent_directory = None
    directory.name = 'root'
    directory.path = '/'
    directory.put()

    my_user.root_directory = directory.key
    my_user.put()


def add_directory(name, parent_directory_key, my_user):
    parent_directory_object = parent_directory_key.get()

    path = get_path_for_directory(name, parent_directory_object, my_user)

    directory_id = my_user.key.id() + path
    directory = Directory(id=directory_id)

    # check if directory already exists in this path
    if directory.key not in my_user.directories:
        # Add key to parent directory
        parent_directory_object.directories.append(directory.key)
        parent_directory_object.put()

        # Set all attributes of the directory and save it to datastore
        directory.parent_directory = parent_directory_key
        directory.name = name
        directory.path = path
        directory.put()

        # Add key of this directory to user object
        my_user.directories.append(directory.key)
        my_user.put()


def delete_directory(directory_name, my_user):
    # current directory is the parent directory of the one that will be deleted
    parent_directory_object = get_current_directory_key(my_user).get()

    directory_id = my_user.key.id() + get_path_for_directory(directory_name, parent_directory_object, my_user)
    directory_key = ndb.Key(Directory, directory_id)

    # Delete reference to this object from parent_directory
    parent_directory_object.directories.remove(directory_key)
    parent_directory_object.put()

    # Delete reference from myuser
    my_user.directories.remove(directory_key)
    my_user.put()

    # Delete directory object from datastore
    directory_key.delete()


def delete_file(filename, my_user):
    parent_directory_object = get_current_directory_key(my_user).get()
    file_path = get_path_for_directory(filename, parent_directory_object, my_user)
    file_id = my_user.key.id() + file_path
    file_key = ndb.Key(File, file_id)

    # Delete file key from directory
    parent_directory_object.files.remove(file_key)
    parent_directory_object.put()

    # Delete actual file from blobstore
    blobstore.delete(file_key.get().blob)

    # Delete file object
    file_key.delete()


def navigate_up(my_user):
    if not is_in_root_directory(my_user):
        parent_directory_key = get_parent_directory_key(my_user)
        my_user.current_directory = parent_directory_key
        my_user.put()


def navigate_to_directory(directory_name, my_user):
    parent_directory_object = get_current_directory_key(my_user).get()
    directory_id = my_user.key.id() + get_path_for_directory(directory_name, parent_directory_object, my_user)
    directory_key = ndb.Key(Directory, directory_id)

    my_user.current_directory = directory_key
    my_user.put()


def get_path_for_directory(name, parent_directory_object, my_user):
    if is_in_root_directory(my_user):
        return parent_directory_object.path + name
    else:
        return parent_directory_object.path + '/' + name


# returns true if current directory is root directory
def is_in_root_directory(my_user):
    current_directory = get_current_directory_key(my_user).get()
    return True if current_directory.parent_directory is None else False


# returns key of current directory
def get_current_directory_key(my_user):
    return my_user.current_directory


# returns key of parent directory
def get_parent_directory_key(my_user):
    current_directory = get_current_directory_key(my_user)
    return current_directory.get().parent_directory


def get_login_url(main_page):
    return users.create_login_url(main_page.request.uri)


def get_logout_url(main_page):
    return users.create_logout_url(main_page.request.uri)
