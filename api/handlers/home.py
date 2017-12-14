
import logging

from flask import Flask, render_template, request, abort, session, redirect

from api import app

@app.route('/')
def home():
    # List of handlers
    handlers = [
        ('Meme Form', '/meme'),
        ('Meme API', '/api/meme/1/getlist'),
        ('Download Williamhill', '/williamhill'),
    ]
    return render_template('home.html', parts=handlers)
