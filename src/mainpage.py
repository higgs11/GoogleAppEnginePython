import os
from controlmodule import ControlModule
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
    def get(self):
        controlmodules_query = ControlModule.all()
        controls = controlmodules_query.fetch(10)        

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'controls': controls,
            'url': url,
            'url_linktext': url_linktext,
            }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

class Submit(webapp.RequestHandler):
    def post(self):
        contModule = ControlModule()
      
        if(users.get_current_user()):
            contModule.author = users.get_current_user()
            
        contModule.name = self.request.get('name')
        contModule.deviceid = int(self.request.get('deviceid'))
        
        sameidresults = db.GqlQuery("SELECT * FROM ControlModule WHERE deviceid = :1", contModule.deviceid)
        for result in sameidresults:
            result.delete()
        
        onState = self.request.get('onstate')
        contModule.onstate = ((onState == 'on') or (onState == 'true') or (onState == 'On') or (onState == 'True'))
        
        contModule.put()
        self.redirect('/')
        
class Toggle(webapp.RequestHandler):
    def post(self):
        
        id = int(self.request.get('toggleid'))
        
        sameidresults = db.GqlQuery("SELECT * FROM ControlModule WHERE deviceid = :1", id)
        for result in sameidresults:
            result.onstate = not result.onstate
            result.put()
        
        self.redirect('/')        
  
application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/submit', Submit),
                                      ('/toggle', Toggle)],
                                     debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()