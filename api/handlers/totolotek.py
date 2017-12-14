from flask import Flask, render_template, request, abort, session, redirect, make_response

from api import app
from api.models.match import Match

from bs4 import BeautifulSoup

import logging
import re
import datetime
import requests

#import pandas as pd

@app.route('/totolotek', methods=['GET'])
def download_totolotek():
    url = "https://www.totolotek.pl/zaklady-sportowe?DS=Pi%C5%82ka%20no%C5%BCna"
    logging.info('page: {}'.format(url))

    #http = urllib3.PoolManager()
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find(id="ctl00_CPH_UCBetList_GVBetEvents_DXMainTable")

    times = [time.get_text() for time in table.select(".dxgvDataRow_BlackGlass .gridDate.dxgv")]

    team_homes = [homeTeam.get_text() for homeTeam in table.select(".dxgvDataRow_BlackGlass .gridHomeTeam.dxgv")]
    team_aways = [awayTeam.get_text() for awayTeam in table.select(".dxgvDataRow_BlackGlass .gridAwayTeam.dxgv")]
    odd_homes = [oddHome.get_text().strip().replace(',', '.') for oddHome in
                 table.select(".dxgvDataRow_BlackGlass .gridOddsHome.dxgv")]
    odd_draws = [oddDraw.get_text().strip().replace(',', '.') for oddDraw in
                 table.select(".dxgvDataRow_BlackGlass .gridOddsDraw.dxgv")]
    odd_aways = [oddAway.get_text().strip().replace(',', '.') for oddAway in
                 table.select(".dxgvDataRow_BlackGlass .gridOddsAway.dxgv")]



    groups = [league.get_text() for league in table.select(".dxgvGroupRow_BlackGlass .dxgv")]

    how_many_in_group = []
    data_list = []

    for i in xrange(0, len(groups) - 1):
        if (len(groups[i]) > 9 and groups[i][0] == 'D'):
            data = str(groups[i])
            data = data[6:16]
        elif (len(groups[i]) > 9 and groups[i][-2].isdigit()):
            how_many_in_group.append(groups[i][-2])
            data_list.append(data)

    how_many_in_group = [int(el) for el in how_many_in_group]

    league_list = []

    for i in range(len(groups) - 1):
        if (len(groups[i]) > 9 and groups[i][-2].isdigit() and groups[i][0] != 'D'):
            league = groups[i].lstrip("Rozgrywki: ")
            league = league.rstrip("(0123456789)")
            league = league.strip()
            league_list.append(league)

    leagues = []
    j = 0
    for how_many in how_many_in_group:
        # print how_many
        for i in range(how_many):
            leagues.append(league_list[j])
        j = j + 1


    datetimes = []
    j = 0
    k = 0
    for how_many in how_many_in_group:
        for i in range(how_many):
            datetime = data_list[j] + ' ' + times[k]
            datetimes.append(datetime)
            k = k + 1
        j = j + 1


    ret = ""
    i = 0
    ret += ( "{} {}".format(len(datetimes), len(team_aways)) )
    for e in team_homes:
        ret += ( "{}  {} - {} <br>".format(i, team_homes[i], team_aways[i]) )
        i += 1

    #todo list of different sizes --> resolve


    # # Save the parameters in the datastore
    # s = Search(content='high={}+low={}'.format(alto,basso))
    # s.put()

    return ret
