import webapp2
import logging
from google.appengine.ext import ndb
import renderer
import utilities
from directory import Directory


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

            # set current path on login to root directory
            my_user.current_directory = ndb.Key(Directory, my_user.key.id() + '/')
            my_user.put()

            renderer.render_main(self, utilities.get_logout_url(self), my_user.directories,
                                 utilities.get_current_directory_key(my_user).get().path)

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


# starts the web application and specifies the routing table
app = webapp2.WSGIApplication(
    [
        ('/', MainPage),
    ], debug=True)
