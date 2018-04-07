from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import utilities
import logging


class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        uploads = self.get_uploads()

        # upload all the files that came in the request
        for upload in uploads:
            # Get file name from the info of the file
            filename = blobstore.BlobInfo(upload.key()).filename

            utilities.add_file(upload, filename)

        self.redirect('/')
