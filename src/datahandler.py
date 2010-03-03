from controlmodule import ControlModule

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


class Data(webapp.RequestHandler):
    def get(self):
        controlmodules_query = ControlModule.all()
        controls = controlmodules_query.fetch(10)        
        self.response.out.write('{"Outlets": [')        
        count = 0;
        for control in controls:    
            if(count > 0):
                self.response.out.write(',')
            count = count + 1
            onString = '' 
            if(control.onstate):
                onString = 'true'
            else:
                onString = 'false'
            self.response.out.write('{id:%s,value:%s}' % (control.deviceid, onString))
        
        self.response.out.write(']}')
        
class Power(webapp.RequestHandler):
    def post(self):                
        id = int(self.request.get('powerid'))
        power = float(self.request.get('power'))
        
        sameidresults = db.GqlQuery("SELECT * FROM ControlModule WHERE deviceid = :1", id)
        for result in sameidresults:
            result.power = power
            result.put()        
            
            

application = webapp.WSGIApplication(
                                     [('/data', Data),
                                      ('/power', Power)],
                                     debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()