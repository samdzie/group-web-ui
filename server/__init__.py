"""A Flask API for the web app."""

import random
import string
from datetime import datetime, timedelta
from flask import Flask, jsonify, make_response, url_for


app = Flask(__name__)


def random_event():
    """Generate a random event object.

    The event begins at a random time in 2020 and lasts for a random
    multiple of 15 minutes in the range of 15 minutes to 4 hours.
    """
    title = ''.join(random.choices(string.ascii_lowercase, k=10))
    start_ts = datetime(year=2020, month=1, day=1).timestamp()
    end_ts = datetime(year=2020, month=12, day=31).timestamp()
    start_ts = start_ts + random.random() * (end_ts - start_ts)
    start = datetime.fromtimestamp(start_ts)
    end = start + timedelta(minutes=(15 * random.randint(1, 16)))
    return {
        'title' : title,
        'start' : start,
        'end' : end
    }


@app.route('/api')
def hello_world():
    """A welcome message to verify a connection to the API."""
    return 'Welcome to the API!'


@app.route('/api/group/<group_id>/events')
def get_events(group_id):
    """Return a list of all stored events in ascending order of start
    time."""
    events = {
        'events' : [random_event() for _ in range(10)]
    }
    events['events'] = sorted(events['events'], key=lambda x: x['start'])
    response = make_response(events)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/api/group/<group_id>/home')
def get_group_home(group_id):
    """Return a JSON object containing the group's name, welcome
    message, about text, and a URL to its icon."""
    filename = random.choice([
        '35411434.png',
        '57271680.png',
        '62537138.png',
    ])
    group_info = {
        'name' : 'Group ' + group_id,
        'welcome' : ' '.join(''.join(
            random.choices(string.ascii_lowercase, k=5)) for _ in range(50)),
        'about' : ' '.join(''.join(
            random.choices(string.ascii_lowercase, k=5)) for _ in range(50)),
        'icon' : ('http://localhost:5000' +
            url_for('static', filename=filename))
    }
    response = make_response(group_info)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
