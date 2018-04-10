from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.ext import blobstore
from myuser import MyUser
from directory import Directory
from file import File
import logging
import re


# Get user from this page
def get_user():
    return users.get_current_user()


# get user from data
def get_my_user():
    user = get_user()
    if user:
        my_user_key = ndb.Key(MyUser, user.user_id())
        return my_user_key.get()


def get_directories_in_current_path():
    return get_current_directory_object().directories


def get_files_in_current_path():
    return get_current_directory_object().files


def get_file_object(filename):
    my_user = get_my_user()

    parent_directory_object = get_current_directory_object()
    file_path = get_path(filename, parent_directory_object)
    file_id = my_user.key.id() + file_path
    file_key = ndb.Key(File, file_id)
    return file_key.get()


def is_user_logged_in():
    return True if get_user() else False


# returns true if for this user a myuser object already exists in the datastore
def user_exists():
    return True if get_my_user() else False


def add_new_user(user):
    my_user = MyUser(id=user.user_id())
    add_root_directory(my_user)

    # set current path on first login to root directory
    my_user.current_directory = ndb.Key(Directory, my_user.key.id() + '/')
    my_user.put()


def add_root_directory(my_user):
    directory_id = my_user.key.id() + '/'
    directory = Directory(id=directory_id)

    directory.parent_directory = None
    directory.name = 'root'
    directory.path = '/'
    directory.put()

    my_user.root_directory = directory.key
    my_user.put()


def add_directory(name, parent_directory_key):
    my_user = get_my_user()

    parent_directory_object = parent_directory_key.get()

    path = get_path(name, parent_directory_object)

    directory_id = my_user.key.id() + path
    directory = Directory(id=directory_id)

    # check if directory already exists in this path
    if exists(directory.key, parent_directory_object.directories):
        # Add key to parent directory
        parent_directory_object.directories.append(directory.key)
        parent_directory_object.put()

        # Set all attributes of the directory and save it to datastore
        directory.parent_directory = parent_directory_key
        directory.name = name
        directory.path = path
        directory.put()


def add_file(upload, filename):
    my_user = get_my_user()
    current_directory_object = get_current_directory_object()
    file_id = my_user.key.id() + get_path(filename, current_directory_object)
    file_key = ndb.Key(File, file_id)

    if exists(file_key, current_directory_object.files):
        file_object = File(id=file_id)
        file_object.name = filename
        file_object.blob = upload.key()
        file_object.put()

        current_directory_object.files.append(file_key)
        current_directory_object.put()

    else:
        # Delete uploaded file from the blobstore
        blobstore.delete(upload.key())
        logging.debug('A file with this name already exists in this directory!')


def delete_directory(directory_name):
    my_user = get_my_user()

    # current directory is the parent directory of the one that will be deleted
    parent_directory_object = get_current_directory_object()

    directory_id = my_user.key.id() + get_path(directory_name, parent_directory_object)
    directory_key = ndb.Key(Directory, directory_id)
    directory_object = directory_key.get()

    if is_directory_empty(directory_object):
        # Delete reference to this object from parent_directory
        parent_directory_object.directories.remove(directory_key)
        parent_directory_object.put()

        # Delete directory object from datastore
        directory_key.delete()


def delete_file(filename):
    my_user = get_my_user()

    parent_directory_object = get_current_directory_object()
    file_path = get_path(filename, parent_directory_object)
    file_id = my_user.key.id() + file_path
    file_key = ndb.Key(File, file_id)

    # Delete file key from directory
    parent_directory_object.files.remove(file_key)
    parent_directory_object.put()

    # Delete actual file from blobstore
    blobstore.delete(file_key.get().blob)

    # Delete file object
    file_key.delete()


def navigate(directory_name):
    if directory_name == "../":
        navigate_up()
    else:
        navigate_to_directory(directory_name)


def navigate_up():
    my_user = get_my_user()

    if not is_in_root_directory():
        parent_directory_key = get_parent_directory_key()
        my_user.current_directory = parent_directory_key
        my_user.put()


def navigate_to_directory(directory_name):
    my_user = get_my_user()

    parent_directory_object = get_current_directory_object()
    directory_id = my_user.key.id() + get_path(directory_name, parent_directory_object)
    directory_key = ndb.Key(Directory, directory_id)

    my_user.current_directory = directory_key
    my_user.put()


def get_path(name, parent_directory_object):
    if is_in_root_directory():
        return parent_directory_object.path + name
    else:
        return parent_directory_object.path + '/' + name


# returns true if current directory is root directory
def is_in_root_directory():
    current_directory = get_current_directory_object()
    return True if current_directory.parent_directory is None else False


def is_directory_empty(directory):
    return not directory.files and not directory.directories


# checks if a key is in a list of keys, if so returns true
def exists(key, key_list):
    return key not in key_list


# returns key of current directory
def get_current_directory_key():
    my_user = get_my_user()
    return my_user.current_directory


# returns key of current directory
def get_current_directory_object():
    return get_current_directory_key().get()


# returns key of parent directory
def get_parent_directory_key():
    current_directory = get_current_directory_key()
    return current_directory.get().parent_directory


# Remove all '/' and ';' from the directory name and leading whitespaces
def prepare_directory_name(directory_name):
    return re.sub(r'[/;]', '', directory_name).lstrip()


# returns a given list in alphabetical order, sorted by attribute name
def sort_list(list_input):
    return sorted(list_input, key=lambda element: element.get().name.lower())


# extracts all the names from a list of directory/ file keys
def get_names_from_list(elements):
    names = list()

    for element in elements:
        names.append(element.get().name)

    return names


def get_login_url(main_page):
    return users.create_login_url(main_page.request.uri)


def get_logout_url(main_page):
    return users.create_logout_url(main_page.request.uri)
