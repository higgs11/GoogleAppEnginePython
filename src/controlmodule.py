from google.appengine.ext import db

class ControlModule(db.Model):
    author = db.UserProperty()
    deviceid = db.IntegerProperty()
    power = db.FloatProperty()
    onstate = db.BooleanProperty()
    name = db.StringProperty()   
    date = db.DateTimeProperty(auto_now_add=True)