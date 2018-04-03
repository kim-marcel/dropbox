import webapp2
import logging
import renderer
import utilities
from uploadhandler import UploadHandler
from downloadhandler import DownloadHandler
from google.appengine.ext import blobstore


class MainPage(webapp2.RequestHandler):
    # GET-request
    def get(self):
        logging.debug("GET")
        self.response.headers['Content-Type'] = 'text/html'

        # check whether user is logged in
        if utilities.user_is_logged_in():
            # if myuser object is None --> No user with key found --> new user --> make new user in datastore
            if not utilities.user_exists():
                utilities.add_new_user(utilities.get_user())

            directories_in_current_path = utilities.get_directories_in_current_path()
            files_in_current_path = utilities.get_files_in_current_path()

            renderer.render_main(self,
                                 utilities.get_logout_url(self),
                                 directories_in_current_path,
                                 files_in_current_path,
                                 utilities.get_current_directory_key().get().path,
                                 utilities.is_in_root_directory(),
                                 blobstore.create_upload_url('/upload'))

        # if no user is logged in create login url
        else:
            renderer.render_login(self, utilities.get_login_url(self))

    # POST-request
    def post(self):
        logging.debug("POST")
        self.response.headers['Content-Type'] = 'text/html'

        button_value = self.request.get('button')

        if button_value == 'Add':
            directory_name = self.request.get('value')
            utilities.add_directory(directory_name, utilities.get_current_directory_key())
            self.redirect('/')

        elif button_value == 'Delete':
            directory_name = self.request.get('directory_name')
            filename = self.request.get('file_name')

            if directory_name == "":
                utilities.delete_file(filename)
            else:
                utilities.delete_directory(directory_name)

            self.redirect('/')

        elif button_value == 'Navigate':
            directory_name = self.request.get('directory_name')
            utilities.navigate_to_directory(directory_name)
            self.redirect('/')

        elif button_value == 'Up':
            utilities.navigate_up()
            self.redirect('/')


# starts the web application and specifies the routing table
app = webapp2.WSGIApplication(
    [
        ('/', MainPage),
        ('/upload', UploadHandler),
        ('/download', DownloadHandler)
    ], debug=True)
