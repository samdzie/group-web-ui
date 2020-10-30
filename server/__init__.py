"""A Flask API for the web app."""

import random
import string
from datetime import datetime, timedelta
import requests
from flask import Flask, jsonify, make_response, send_from_directory, url_for


app = Flask(__name__)
app.config['GROUP_SERVER_HOST'] = 'http://127.0.0.1:5001'
app.config['EVENT_SERVER_HOST'] = 'http://127.0.0.1:5002'


@app.route('/')
def send_homepage():
    """Send index.html from the built Vue app."""
    return send_from_directory('dist', 'index.html')


@app.route('/js/<path:path>')
def send_js(path):
    """Send JavaScript files from the built Vue app."""
    return send_from_directory('dist/js', path)


@app.route('/css/<path:path>')
def send_css(path):
    """Send CSS files from the built Vue app."""
    return send_from_directory('dist/css', path)


@app.route('/favicon.ico')
def send_favicon():
    """Send the favicon from the built Vue app."""
    return send_from_directory('dist', 'favicon.ico')


@app.route('/api')
def hello_world():
    """A welcome message to verify a connection to the API."""
    return 'Welcome to the API!'


@app.route('/api/group/<group_id>/events')
def get_events(group_id):
    """Return a list of all stored events in ascending order of start
    time."""
    request_url = app.config['EVENT_SERVER_HOST'] + '/group/' + group_id
    group_events = requests.get(request_url).json()
    response = make_response(group_events)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/api/group/<group_id>/home')
def get_group_home(group_id):
    """Return a JSON object containing the group's name, welcome
    message, about text, and a URL to its icon."""
    request_url = app.config['GROUP_SERVER_HOST'] + '/group/' + group_id
    group_info = requests.get(request_url).json()
    response = make_response(group_info)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
