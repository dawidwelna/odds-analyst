import logging
import json
import urllib2, urllib

from flask import Flask, render_template, request, abort, session, redirect, make_response

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import URL, Email, required, ValidationError, length

from datetime import datetime
from api import app
from google.appengine.ext import ndb
from api.models.search import Search


@app.route('/api/meme/1/getlist',methods=['GET'])
def api_meme():
    json_response = {}
    # return last 10 searches
    searches = Search.query().order(-Search.date).fetch(10)
    json_response['data'] = []
    for s in searches:
        json_response['data'].append({
            'content':s.content,
            'month':s.date.month,
            'year': s.date.year})

    # status of the json_response
    json_response['status'] = 'success'
    # success or error message
    json_response['message'] = 'Successfully returned the resource'
    logging.info(json_response)
    response =  make_response(json.dumps(json_response,ensure_ascii=True),200)

    # important: setting header type
    response.headers['content-type']='application/json'
    return response


def raise_error(
    message='An error occurred during the request',
    errorcode=500):
        json_response = {}
        # status of the json_response
        json_response['status'] = 'failure'
        # success or error message
        json_response['message'] = message
        json_response['data'] = []
        response =    make_response(json.dumps(json_response,ensure_ascii=True),errorcode)
        response.headers['content-type']='application/json'
        return response


@app.route('/api/meme/1/getfilteredlist',methods=['GET'])
def api_meme_filtered():
    # getting and checking input parameters
    parameters = request.args.keys()
    logging.info('parameters: {}'.format(parameters))

    # ################
    # Check errors
    # ################
    allowed_parameters = ['month','year']
    required_parameters = ['month','year']
    allowed_types = {'month': int, 'year': int}
    for r in required_parameters:
        if r not in parameters:
            return raise_error(message='Parameter "{}" is missing'.format(r))
        try:
            # es: int('10m')
            allowed_types[r](request.args[r])
        except ValueError:
            return raise_error(message='Parameter "{}" must be {}'.format(r,allowed_types[r]))

    month = int(request.args['month'])
    year = int(request.args['year'])

    # ####################
    # Build response
    # ####################
    json_response = {}

    start_date = datetime.strptime('01/{:02d}/{:04d}'.format(month,year), '%d/%m/%Y')

    if month == 12:
        end_date = datetime.strptime('01/{:02d}/{:04d}'.format((month+1 )%12,year+1), '%d/%m/%Y')
    else:
        end_date = datetime.strptime('01/{:02d}/{:04d}'.format(month+1,year), '%d/%m/%Y')

    logging.info('start: {}, end; {}'.format(start_date, end_date))

    searches = Search.query(
        ndb.AND(
            Search.date >= start_date,
            Search.date < end_date
            )
        )

    json_response = {}
    json_response['data'] = []
    for s in searches.iter():
        json_response['data'].append({
            'content':s.content,
            'month':s.date.month,
            'year': s.date.year})

    # status of the json_response
    json_response['status'] = 'success'
    # success or error message
    json_response['message'] = 'Successfully returned the resource'
    logging.info(json_response)
    response =  make_response(json.dumps(json_response,ensure_ascii=True),200)

    # important: setting header type
    response.headers['content-type']='application/json'
    return response
