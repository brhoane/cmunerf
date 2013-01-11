import webapp2
import traceback
import cgi
from google.appengine.ext import db
from google.appengine.api import users

class UserData(db.Model):
  name = db.StringProperty(required=True)
  email = db.StringProperty(required=True)
  target = db.StringProperty()


class MyHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    ud = UserData.get_or_insert(user.user_id(),name=user.nickname(),email=user.email())

    greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)</br>Your target is: %s</br><a href=\"/admin/\">Admin Section</a>" %
              (user.nickname(), users.create_logout_url("/"), ud.target))

    self.response.out.write("<html><body>%s</body></html>" % greeting)

class AdminHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    greeting = ("Welcome, %s! You're in the admin section! (<a href=\"%s\">sign out</a>)" %
              (user.nickname(), users.create_logout_url("/")))

    self.response.out.write("<html><body>%s</body></html>" % greeting)


app = webapp2.WSGIApplication([('/', MyHandler), ('/admin/', AdminHandler)], debug=True)