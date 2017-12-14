# -*- encoding: utf8 -*-

import os

from google.appengine.ext import vendor

import tempfile
tempfile.SpooledTemporaryFile = tempfile.TemporaryFile

vendor.add('lib')

# we set a GAE_DEV variable to know if we are running on the local development environment
# https://cloud.google.com/appengine/docs/standard/python/tools/using-local-server#detecting_application_runtime_environment
if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
	GAE_DEV = False
else:
	GAE_DEV = True
