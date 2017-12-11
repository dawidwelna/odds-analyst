import logging

from flask import Flask, render_template, request, abort, session, redirect, make_response

from api import app

# server error
@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return 'SERVER ERROR: An internal error occurred.', 500

# not found
@app.errorhandler(404)
def not_found(e):
    logging.exception(e)
    return 'SERVER ERROR: An internal error occurred.', 404

# method not allowed
@app.errorhandler(405)
def not_found(e):
    logging.exception(e)
    return 'SERVER ERROR: An internal error occurred.', 405
