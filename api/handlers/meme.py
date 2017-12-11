import logging

from flask import Flask, render_template, request, abort, session, redirect, make_response

import urllib2, urllib

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import URL, Email, required, ValidationError, length

from api import app
from api.models.search import Search

MASHAPE_KEY = "<your-mashape-key>"

class MemeForm(FlaskForm):
    text_high = StringField('Testo in alto', [required()])
    text_low = StringField('Testo in basso', [required()])
    submit = SubmitField('Submit', [required()])

@app.route('/meme', methods=['GET'])
def showmemeform():
    form = MemeForm()
    url = '/'
    return render_template('meme.html', form=form)

@app.route('/meme', methods=['POST'])
def meme_submit():

    form = MemeForm(request.form)
    if not form.validate():
        return render_template('meme.html', form=form), 400


    alto = form.text_high.data
    basso = form.text_low.data

    # Save the parameters in the datastore
    s = Search(content='high={}+low={}'.format(alto,basso))
    s.put()

    logging.info('Alto: {}, Basso: {}'.format(alto,basso))

    url = "https://ronreiter-meme-generator.p.mashape.com/meme"
    fields = {
        "top": alto,
        "bottom": basso,
        "font": "Impact",
        "font_size": 50,
        "meme": "Grumpy Cat"
    }
    params = urllib.urlencode(fields)
    myurl = '{}?{}'.format(url, params)
    logging.info('myurl: {}'.format(myurl))
    req = urllib2.Request(myurl)
    req.add_header("X-Mashape-Key", MASHAPE_KEY)
    req.add_header("Accept", "image/jpeg")
    urlresponse = urllib2.urlopen(req)
    content = urlresponse.read()
    response = make_response(content)
    response.headers['content-type'] = "image/jpeg"
    return response
