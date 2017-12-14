from flask import Flask, render_template, request, abort, session, redirect, make_response

from api import app
from api.models.match import Match

import logging
import re
import datetime
import requests


@app.route('/mashapeodds', methods=['GET'])
def download_mashapeodds():
    url = 'https://bettingodds-bettingoddsapi-v1.p.mashape.com/events/2017-12-15'
    logging.info('page: {}'.format(url))

    response = requests.get(url,
                           headers={
                               "X-Mashape-Key": "your key",
                               "Accept": "application/json"
                           }
                           )


    return response.content
