from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
from file import File
import utilities


class DownloadHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):
        filename = self.request.get('file_name')

        my_user = utilities.get_my_user()

        parent_directory_object = utilities.get_current_directory_key(my_user).get()
        file_path = utilities.get_path_for_directory(filename, parent_directory_object, my_user)
        file_id = my_user.key.id() + file_path
        file_key = ndb.Key(File, file_id)
        file_object = file_key.get()

        self.send_blob(file_object.blob)
