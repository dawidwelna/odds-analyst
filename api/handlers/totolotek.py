from flask import Flask, render_template, request, abort, session, redirect, make_response

from api import app
from api.models.match import Match

import requests
from bs4 import BeautifulSoup

import sys
import logging
import re
import datetime

reload(sys)
sys.setdefaultencoding('utf8')

@app.route('/totolotek', methods=['GET'])
def download_totolotek():
    url = "https://www.totolotek.pl/zaklady-sportowe?DS=Pi%C5%82ka%20no%C5%BCna"

    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    table = soup.find(class_="dxgvTable_BlackGlass")
    row_list = table.find_all('tr')

    league = "NO LEAGUE"
    date = "Unknown"

    ret = ""
    for row in row_list:
        try:
            if (row['class']):
                if row['class'][0] == "dxgvGroupRow_BlackGlass":
                    # league and data row here
                    cell_list = row.find_all('td')
                    try:
                        # only league row has 3 cells
                        league = cell_list[2].get_text()
                        league = league.lstrip("Rozgrywki: ")
                        league = league.rstrip("(Continued on the next page)")
                        league = league.rstrip("(0123456789)")
                        league = league.strip()
                    except IndexError:
                        # IndexError means also that this is data row (we can get data here)
                        date = cell_list[1].get_text()
                        date = date.lstrip("Data: ")
                        date = date.rstrip("(Continued on the next page)")
                        date = date.rstrip("(0123456789)")
                        date = date.strip()
                        #print date
                elif row['class'][0] == "dxgvDataRow_BlackGlass":
                    # match row now

                    cell_list = row.find_all('td')
                    try:
                        hour = cell_list[3].get_text()
                        odd_home = float(cell_list[7].a.get_text().replace(',', '.'))
                        odd_draw = float(cell_list[8].a.get_text().replace(',', '.'))
                        odd_away = float(cell_list[9].a.get_text().replace(',', '.'))
                        team_home = str(cell_list[5].get_text())
                        team_away = str(cell_list[6].get_text())
                        ret += ("{} {} {}  {} - {}  {} {} {} <br><br>".format(date, hour, league, team_home,\
                                                                              team_away, odd_home, odd_draw, odd_away))
                        '''m = Match(
                                league = league,
                                odd_home = odd_home,
                                odd_draw = odd_draw,
                                odd_away = odd_away,
                                team_home = team_home,
                                team_away = team_away,
                                bookmaker='totolotek',
                                bookmaker_country = 'Poland')
                        m.put()'''

                    except AttributeError:
                        continue

        except KeyError:
            # if the row doesn't have key called "class"
            continue

    return ret


