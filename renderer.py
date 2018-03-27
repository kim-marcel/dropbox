import jinja2
import os
import utilities

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


def render_login(self, url):
    template_values = {'url': url}

    template = JINJA_ENVIRONMENT.get_template('/templates/login.html')
    self.response.write(template.render(template_values))


def render_main(self, url):
    template_values = {
        'url': url,
        'user': utilities.get_user(),
    }

    template = JINJA_ENVIRONMENT.get_template('/templates/main.html')
    self.response.write(template.render(template_values))
