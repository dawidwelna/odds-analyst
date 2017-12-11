import logging
from flask import Flask
from flask_wtf.csrf import CSRFProtect

import appengine_config
import api.app_config

app = Flask(__name__)
app.config.from_object(__name__)

# The app.secret_key is required by Flask to sign the CSRF token
if appengine_config.GAE_DEV:
    logging.warning('Using a dummy secret key')
    app.secret_key = 'my-secret-key'
else:
    app.secret_key = myapp.app_config.app_secret_key

# Protecting app from CSRF
CSRFProtect(app)
