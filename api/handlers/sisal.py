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
    url = 'http://sports.williamhill.it/bet_ita/it/betting/y/5/tm/0/Calcio.html'
    logging.info('page: {}'.format(url))

    #http = urllib3.PoolManager()
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    events = soup.select(('div[id^="ip_type_"]'))

    ret = ""

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
            ret += (league + '<br>' + cols[2].text + '<br>')
            ret += ( cols[4].text + ' ' + cols[5].text + ' ' + cols[6].text + '<br><br>' )


    # # Save the parameters in the datastore
    # s = Search(content='high={}+low={}'.format(alto,basso))
    # s.put()

    return ret
