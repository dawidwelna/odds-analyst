from google.appengine.ext import ndb

class Match(ndb.Model):
    date = ndb.DateTimeProperty(auto_now_add=True)

    match_datetime = ndb.DateTimeProperty(indexed=False) # dt_format = "%Y-%m-%d %H:%M"

    league = ndb.StringProperty(indexed=False)
    team_home = ndb.StringProperty(indexed=False)
    team_away = ndb.StringProperty(indexed=False)

    odd_home = ndb.FloatProperty(indexed=False)
    odd_draw = ndb.FloatProperty(indexed=False)
    odd_away = ndb.FloatProperty(indexed=False)

    bookmaker = ndb.StringProperty(indexed=False)
    bookmaker_country = ndb.StringProperty(indexed=False)

    team_home_id = ndb.IntegerProperty(indexed=False)
    team_away_id = ndb.IntegerProperty(indexed=False)

    match_id = ndb.StringProperty(indexed=False) # eg. 1_2_20171221   (will be made of team_home_id, team_away_id, match_datetime)
