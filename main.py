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
        logging.debug('GET')
        self.response.headers['Content-Type'] = 'text/html'

        # check whether user is logged in
        if utilities.is_user_logged_in():
            # if myuser object is None --> No user with key found --> new user --> make new user in datastore
            if not utilities.user_exists():
                utilities.add_new_user(utilities.get_user())

            directory_name = self.request.get('directory_name')

            # Navigate to a directory sent in the url via get request
            if directory_name != '':
                utilities.navigate(directory_name)
                self.redirect('/')

            # get all directories and files in the current path
            directories_in_current_path = utilities.get_directories_in_current_path()
            files_in_current_path = utilities.get_files_in_current_path()

            # sort all directories and files alphabetically
            directories_in_current_path = utilities.sort_list(directories_in_current_path)
            files_in_current_path = utilities.sort_list(files_in_current_path)

            # extract file and directory names from the key list
            # so that only the names have to be send to the gui and not the whole object
            directories_in_current_path = utilities.get_names_from_list(directories_in_current_path)
            files_in_current_path = utilities.get_names_from_list(files_in_current_path)

            renderer.render_main(self,
                                 utilities.get_logout_url(self),
                                 directories_in_current_path,
                                 files_in_current_path,
                                 utilities.get_current_directory_object().path,
                                 utilities.is_in_root_directory(),
                                 blobstore.create_upload_url('/upload'))

        # if no user is logged in create login url
        else:
            renderer.render_login(self, utilities.get_login_url(self))

    # POST-request
    def post(self):
        logging.debug('POST')
        self.response.headers['Content-Type'] = 'text/html'

        button_value = self.request.get('button')

        if button_value == 'Add':
            self.add()
            self.redirect('/')

        elif button_value == 'Delete':
            self.delete()
            self.redirect('/')

        elif button_value == 'Up':
            utilities.navigate_up()
            self.redirect('/')

        elif button_value == 'Home':
            utilities.navigate_home()
            self.redirect('/')

    def add(self):
        directory_name = self.request.get('value')
        directory_name = utilities.prepare_directory_name(directory_name)
        if not (directory_name is None or directory_name == ''):
            utilities.add_directory(directory_name, utilities.get_current_directory_key())

    def delete(self):
        name = self.request.get('name')
        kind = self.request.get('kind')

        if kind == 'file':
            utilities.delete_file(name)
        elif kind == 'directory':
            utilities.delete_directory(name)


# starts the web application and specifies the routing table
app = webapp2.WSGIApplication(
    [
        ('/', MainPage),
        ('/upload', UploadHandler),
        ('/download', DownloadHandler)
    ], debug=True)
