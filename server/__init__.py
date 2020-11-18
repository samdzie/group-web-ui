"""A Flask API for the web app."""

import random
import string
from datetime import datetime, timedelta
import requests
from flask import (abort, Flask, jsonify, make_response, request,
    send_from_directory, url_for)


app = Flask(__name__)
app.config.from_object('server.config')


def is_connected(url):
    """Return True if a connection can be established with url, return
    False otherwise."""
    try:
        return requests.get(url).ok
    except requests.ConnectionError:
        return False


def service_connections():
    """Return a dict from service names to booleans indicating whether
    a connection can be established with their hosts."""
    urls = {
        'home'  : app.config['GROUP_SERVER_HOST'] + '/api/homepage/docs',
        'event' : app.config['EVENT_SERVER_HOST'] + '/',
        'image' : app.config['IMAGE_SERVER_HOST'] + '/images/docs',
    }
    return {x: is_connected(y) for (x,y) in urls.items()}


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
def send_service_connections():
    """Send the dict returned by service_connections as a JSON object."""
    return jsonify(service_connections())


@app.route('/api/group', methods=['POST'])
def create_group():
    """Create a group.

    The POST request should contain JSON with the following attributes:
    name    the group's name
    welcome the group's welcome message
    about   the group's about section
    """
    if not service_connections()['home']:
        app.logger.error('cannot connect to homepage server')
        abort(500)
    if request.json is None or not 'name' in request.json:
        abort(400)
    request_url = app.config['GROUP_SERVER_HOST'] + '/api/homepage/'
    data = {
        'group_name' : request.json.get('name'),
        'welcome_message' : request.json.get('welcome'),
        'about_section' : request.json.get('about')
    }
    resp = requests.post(request_url, json=data)
    return jsonify(resp.json()), resp.status_code


@app.route('/api/group/<group_id>/events')
def get_events(group_id):
    """Return a list of all stored events in ascending order of start
    time."""
    if not service_connections()['event']:
        app.logger.error('cannot connect to events server')
        abort(500)
    request_url = app.config['EVENT_SERVER_HOST'] + '/group/' + group_id
    group_events = requests.get(request_url).json()
    return jsonify(group_events)


@app.route('/api/group/<group_id>/home')
def get_group_home(group_id):
    """Return a JSON object containing the group's name, welcome
    message, about text, and a URL to its icon."""
    if not service_connections()['home']:
        app.logger.error('cannot connect to homepage server')
        abort(500)
    request_url = app.config['GROUP_SERVER_HOST'] + '/api/homepage/' + group_id
    try:
        upstream = requests.get(request_url).json()
    except ValueError:
        app.logger.error('No valid JSON returned from homepage service')
        abort(500)
    downstream = {
        'id' : group_id,
        'name' : upstream.get('group_name'),
        'welcome' : upstream.get('welcome_message'),
        'about' : upstream.get('about_section'),
    }
    return jsonify(downstream)


@app.route('/api/group/<group_id>/home', methods=['PUT'])
def edit_group_home(group_id):
    """Update the group service."""
    if not service_connections()['home']:
        app.logger.error('cannot connect to homepage server')
        abort(500)
    data = {}
    if request.json is None:
        abort(400)
    if 'name' in request.json:
        data['group_name'] = request.json['name']
    if 'welcome' in request.json:
        data['welcome_message'] = request.json['welcome']
    if 'about' in request.json:
        data['about_section'] = request.json['about']
    request_url = app.config['GROUP_SERVER_HOST'] + '/api/homepage/' + group_id
    resp = requests.patch(request_url, json=data)
    return 'passed', resp.status_code
