import wsgiref.handlers
import os
import cgi
import functools
import random
import friendfeed

from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import mail
from datetime import datetime

from django.utils import feedgenerator

class MainPage(webapp.RequestHandler):
  def get(self):
	service = friendfeed.FriendFeed()
	feed = service.search("who:bjtitus service:internal")
	for entry in feed ["entries"]:
		#self.response.out.write('<p>' + entry["title"] + '</p>')
		#self.response.out.write(entry["updated"])
		#self.response.out.write(entry["service"]["id"])
		if len(entry["media"]) is 1:
			self.response.out.write('<img src="' + entry["media"][0]["thumbnails"][0]["url"] + '">')
		self.response.out.write('<br/>')

def administrator(method):
  @functools.wraps(method)
  def wrapper(self, *args, **kwargs):
    user = users.get_current_user()
    if not user:
      if self.request.method == "GET":
        self.redirect(users.create_login_url(self.request.uri))
        return
      self.error(404)
    elif not users.is_current_user_admin():
      self.error(404)
    else:
      return method(self, *args, **kwargs)
  return wrapper

"""class Feed(EntryHandler):
    def get(self):
        feed = self._format(
            title=u"Class of '08 Board",
            link=u"http://montgomerybell.edu",
            description=u"Feed of all posts on the site",
            language=u"en",
        )
        for user in User.all().order('-published').fetch(limit=10):
            feed.add_item(title=user.name, link="/entry/" + str(user.key()),
                          description=user.email)
        feed.write(self.response.out, 'utf-8')

class AtomFeed(Feed):
    _format = feedgenerator.Atom1Feed

class RssFeed(Feed):
    _format = feedgenerator.Rss201rev2Feed
"""
def main():
  application = webapp.WSGIApplication(
                                       [('/', MainPage),
										#('/rss', RssFeed),
										#('/atom', AtomFeed),
										],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
  main()