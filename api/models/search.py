from google.appengine.ext import ndb

class Search(ndb.Model):
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

#     date insert in db
#   match date
#   team_home name
#   team_away name
#   odd_1
#   odd_X
#   odd_2
#   bookmaker
#   country
