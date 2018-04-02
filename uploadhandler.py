from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
from file import File
import utilities
import logging


class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        # Get the data (file) from the request
        upload = self.get_uploads()[0]
        # Get file name from the info of the file
        filename = blobstore.BlobInfo(upload.key()).filename

        my_user = utilities.get_my_user()
        current_directory_object = utilities.get_current_directory_key(my_user).get()
        file_id = my_user.key.id() + utilities.get_path_for_directory(filename, current_directory_object, my_user)
        file_key = ndb.Key(File, file_id)

        if file_key not in current_directory_object.files:
            file_object = File(id=file_id)
            file_object.filename = filename
            file_object.blob = upload.key()
            file_object.put()

            current_directory_object.files.append(file_key)
            current_directory_object.put()

        else:
            # Delete uploaded file from the blobstore
            blobstore.delete(upload.key())
            logging.debug('A file with this name already exists!')

        self.redirect('/')
