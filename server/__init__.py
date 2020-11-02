"""A Flask API for the web app."""

import random
import string
from datetime import datetime, timedelta
import requests
from flask import Flask, jsonify, make_response, send_from_directory, url_for


app = Flask(__name__)
app.config.from_object('server.config')


def check_connection(url):
    """Return True if a connection can be established with url, return
    False otherwise."""
    try:
        return requests.get(url).ok
    except requests.ConnectionError:
        return False


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


@app.route('/api/status')
def service_connections():
    """Return a dict from service names to booleans indicating whether
    a connection can be established with their hosts."""
    urls = {
        'home'  : app.config['GROUP_SERVER_HOST'] + '/api/homepage/docs',
        'event' : app.config['EVENT_SERVER_HOST'] + '/',
        'image' : app.config['IMAGE_SERVER_HOST'] + '/images/docs',
    }
    statuses = {x: check_connection(y) for (x,y) in urls.items()}
    return jsonify(statuses)


@app.route('/api/group/<group_id>/events')
def get_events(group_id):
    """Return a list of all stored events in ascending order of start
    time."""
    request_url = app.config['EVENT_SERVER_HOST'] + '/group/' + group_id
    group_events = requests.get(request_url).json()
    return jsonify(group_events)


@app.route('/api/group/<group_id>/home')
def get_group_home(group_id):
    """Return a JSON object containing the group's name, welcome
    message, about text, and a URL to its icon."""
    request_url = app.config['GROUP_SERVER_HOST'] + '/api/homepage/' + group_id
    upstream = requests.get(request_url).json()
    downstream = {
        'id' : group_id,
        'name' : upstream.get('group_name'),
        'welcome' : upstream.get('welcome_message'),
        'about' : upstream.get('about_section'),
    }
    return jsonify(downstream)
