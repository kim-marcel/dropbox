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

            my_user = utilities.get_my_user()

            directories_in_current_path = utilities.get_directories_in_current_path(my_user)
            files_in_current_path = utilities.get_files_in_current_path(my_user)

            renderer.render_main(self,
                                 utilities.get_logout_url(self),
                                 directories_in_current_path,
                                 files_in_current_path,
                                 utilities.get_current_directory_key(my_user).get().path,
                                 utilities.is_in_root_directory(my_user),
                                 blobstore.create_upload_url('/upload'))

        # if no user is logged in create login url
        else:
            renderer.render_login(self, utilities.get_login_url(self))

    # POST-request
    def post(self):
        logging.debug("POST")
        self.response.headers['Content-Type'] = 'text/html'

        # get user data object from datastore of current user (logged in)
        my_user = utilities.get_my_user()

        button_value = self.request.get('button')

        if button_value == 'Add':
            directory_name = self.request.get('value')
            logging.debug(directory_name + button_value)
            utilities.add_new_directory(directory_name, utilities.get_current_directory_key(my_user), my_user)

            self.redirect('/')

        elif button_value == 'Delete':
            directory_name = self.request.get('directory_name')
            logging.debug('Delete!!!' + directory_name)
            utilities.delete_directory(directory_name, my_user)

            self.redirect('/')

        elif button_value == 'Navigate':
            directory_name = self.request.get('directory_name')
            utilities.navigate_to_directory(directory_name, my_user)
            self.redirect('/')

        elif button_value == 'Up':
            utilities.navigate_up(my_user)
            self.redirect('/')

        elif button_value == 'DeleteFile':
            filename = self.request.get('file_name')
            utilities.delete_file(filename, my_user)
            self.redirect('/')


# starts the web application and specifies the routing table
app = webapp2.WSGIApplication(
    [
        ('/', MainPage),
        ('/upload', UploadHandler),
        ('/download', DownloadHandler)
    ], debug=True)
