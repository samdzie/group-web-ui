"""A Flask API for the web app."""

import requests
from flask import abort, Flask, jsonify, request, send_from_directory


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
        'home'  : app.config['GROUP_SERVER_HOST'] + '/',
        'event' : app.config['EVENT_SERVER_HOST'] + '/api/events/docs',
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
    request_url = app.config['GROUP_SERVER_HOST'] + '/homepage/'
    data = {
        'group_name' : request.json.get('name'),
        'welcome_message' : request.json.get('welcome'),
        'about_section' : request.json.get('about'),
        'events' : []
    }
    resp = requests.post(request_url, json=data)
    if resp.status_code == 201:
        return jsonify(resp.json()), resp.status_code
    return 'passed', resp.status_code


@app.route('/api/group/<group_id>', methods=['DELETE'])
def delete_group(group_id):
    """Delete a group given its ID."""
    if not service_connections()['home']:
        app.logger.error('cannot connect to homepage server')
        abort(500)
    request_url = app.config['GROUP_SERVER_HOST'] + '/homepage/' + group_id
    resp = requests.delete(request_url)
    if resp.status_code == 200:
        return 'deleted', 200
    return 'error ' + str(resp.status_code), resp.status_code


@app.route('/api/group/<group_id>/events', methods=['POST'])
def create_event(group_id):
    """Create a new event and add it to the list of events associated
    with a particular group.

    The POST request should contain JSON with the following attributes:
    title       the title of the event
    description the description of the event
    start       beginning time of the event
    end         end time of the event
    """
    if not service_connections()['event']:
        app.logger.error('cannot connect to events server')
        abort(500)
    request_url = app.config['EVENT_SERVER_HOST'] + '/api/events/'
    data = {
        'title' : 'New event',
        'description' : 'A new event!',
        'start_time' : '01/01/21 12:00 AM',
        'end_time' : '01/01/21 01:00 AM',
        'people' : [],
    }
    resp = requests.post(request_url, json=data)
    if resp.status_code != 201:
        return 'error ' + str(resp.status_code), resp.status_code
    gurl = app.config['GROUP_SERVER_HOST'] + '/homepage/' + group_id
    grsp = requests.get(gurl)
    if grsp.status_code != 200:
        app.logger.error('Error retrieving group ' + group_id)
        return 'error ' + str(grsp.status_code), grsp.status_code
    events = grsp.json().get('events')
    events.append(resp.json().get('id'))
    grsp = requests.patch(gurl, json={'events' : events})
    if grsp.status_code == 200:
        return 'updated', grsp.status_code
    return 'error ' + str(grsp.status_code), grsp.status_code


@app.route('/api/group/<group_id>/events')
def get_events(group_id):
    """Return a list of all stored events in ascending order of start
    time."""
    if not service_connections()['event']:
        app.logger.error('cannot connect to events server')
        abort(500)
    group_url = app.config['GROUP_SERVER_HOST'] + '/homepage/' + group_id
    group_resp = requests.get(group_url)
    if group_resp.status_code != 200:
        app.logger.error('Error retrieving group')
        return 'error ' + group_resp.status_code, group_resp.status_code
    event_ids = group_resp.json().get('events')
    events = []
    for event_id in event_ids:
        event_url = (app.config['EVENT_SERVER_HOST']
            + '/api/events/' + str(event_id) + '/')
        event_resp = requests.get(event_url)
        if event_resp.status_code != 200:
            app.logger.error('Error retrieving event id ' + str(event_id))
            return 'error ' + str(event_resp.status_code), event_resp.status_code
        ejson = event_resp.json()
        events.append({
            'id' : ejson.get('id'),
            'title' : ejson.get('title'),
            'description' : ejson.get('description'),
            'start' : ejson.get('start_time'),
            'end' : ejson.get('end_time'),
        })
    return jsonify(events)


@app.route('/api/group/<group_id>/events/<event_id>', methods=['PUT'])
def update_event(group_id, event_id):
    """Update the event with a given ID."""
    if not service_connections()['event']:
        app.logger.error('cannot connect to events server')
        abort(500)
    request_url = app.config['EVENT_SERVER_HOST'] + '/api/events/' + event_id
    if request.json is None:
        abort(400)
    data = {}
    if request.json.get('title') is not None:
        data['title'] = request.json.get('title')
    if request.json.get('description') is not None:
        data['description'] = request.json.get('description')
    if request.json.get('start') is not None:
        data['start_time'] = request.json.get('start')
    if request.json.get('end') is not None:
        data['end_time'] = request.json.get('end')
    data['people'] = []
    resp = requests.patch(request_url, json=data)
    if resp.status_code == 200:
        return 'updated', 200
    return 'error ' + str(resp.status_code), resp.status_code


@app.route('/api/group/<group_id>/events/<int:event_id>', methods=['DELETE'])
def delete_event(group_id, event_id):
    """Delete the event with a given ID."""
    if not service_connections()['event']:
        app.logger.error('cannot connect to events server')
        abort(500)
    request_url = (
        app.config['EVENT_SERVER_HOST'] + '/api/events/' + str(event_id))
    resp = requests.delete(request_url)
    if resp.status_code != 200:
        app.logger.error('error deleting event ' + str(event_id))
        return 'error ' + str(resp.status_code), resp.status_code
    gurl = app.config['GROUP_SERVER_HOST'] + '/homepage/' + group_id
    grsp = requests.get(gurl)
    if grsp.status_code != 200:
        app.logger.error('error retrieving group ' + str(group_id))
    events = grsp.json().get('events')
    events.remove(event_id)
    grsp = requests.patch(gurl, json={'events' : events})
    if grsp.status_code == 200:
        return 'deleted', 200
    return 'error ' + str(grsp.status_code), grsp.status_code


@app.route('/api/group/<group_id>/home')
def get_group_home(group_id):
    """Return a JSON object containing the group's name, welcome
    message, about text, and a URL to its icon."""
    if not service_connections()['home']:
        app.logger.error('cannot connect to homepage server')
        abort(500)
    request_url = app.config['GROUP_SERVER_HOST'] + '/homepage/' + group_id
    try:
        upstream = requests.get(request_url).json()
    except ValueError:
        app.logger.error('No valid JSON returned from homepage service')
        abort(500)
    if upstream.get('detail') == 'Homepage not found':
        abort(404)
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
    request_url = app.config['GROUP_SERVER_HOST'] + '/homepage/' + group_id
    resp = requests.patch(request_url, json=data)
    return 'passed', resp.status_code
