from flask import Flask, render_template, request, abort, session, redirect, make_response

from api import app
from api.models.match import Match

from bs4 import BeautifulSoup

import logging
import re
import datetime
import requests

@app.route('/williamhill', methods=['GET'])
def download_williamhill():
    ret = ""

    for x in range(0,2):
        url = 'http://sports.williamhill.it/bet_ita/it/betting/y/5/tm/{}/Calcio.html'.format(x)
        logging.info('page: {}'.format(url))

        #http = urllib3.PoolManager()
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        events = soup.select(('div[id^="ip_type_"]'))

        league = "NO LEAGUE"
        for e in events:
            try:
                league = e.find_all('h3')[0].text
            except:
                continue

            rows = e.find_all('tr', attrs={'class': 'rowOdd'} )

            for row in rows:
                cols = row.find_all('td', attrs={'scope': 'col'})

                #ret += ( "{0}<br>".format(datetime.date.today()) )
                ret += "{}  ".format(cols[0].text.encode('utf-8').strip())
                ret += "{}<br>".format(cols[1].text.encode('utf-8').strip())
                ret += "{}<br>".format(league)
                ret += "{}<br>".format(cols[2].text.encode('utf-8').strip())
                ret += "{}<br>".format(cols[4].text.encode('utf-8').strip())
                ret += "{}<br>".format(cols[5].text.encode('utf-8').strip())
                ret += "{}<br>".format(cols[6].text.encode('utf-8').strip())
                ret += "<br><br>"

                teams = cols[2].text.split(" - ")

                # Save the parameters in the datastore
                m = Match(
                    league=league,
                    team_home=teams[0],
                    team_away=teams[1],
                    odd_home=float(cols[4].text),
                    odd_draw=float(cols[5].text),
                    odd_away=float(cols[6].text),
                    bookmaker='williamhill',
                    bookmaker_country="IT")
                #m.put()


    return ret
