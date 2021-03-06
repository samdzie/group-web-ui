import json
import pytest
import server


@pytest.fixture
def client():
    server.app.config['TESTING'] = True
    with server.app.test_client() as client:
        yield client


def test_welcome_message(client):
    rv = client.get('/api')
    assert rv.data == b'Welcome to the API!'


def test_create_group(client):
    info = {
        'name' : 'Group A',
        'welcome' : 'Welcome to Group A!',
        'about' : 'This is what Group A is about.'
    }
    resp = client.post('/api/group', json=info)
    assert resp.status_code == 201


def test_read_group_info(client):
    resp = client.get('/api/group/1/home')
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert data.get('name') == 'Group A'
    assert data.get('welcome') == 'Welcome to Group A!'


def test_edit_group_info(client):
    resp = client.put('/api/group/1/home', json={
        'name' : 'Name',
        'welcome' : 'Welcome',
        'about' : 'About'
    })
    assert resp.status_code == 200


def test_group_events(client):
    resp = client.get('/api/group/1/events')
    assert resp.status_code == 200
    data = json.loads(resp.data)
    events = data.get('events')
    assert events[0].get('name') == 'Breakfast'
    assert events[0].get('start_time') == '11/01/2020 09:00 AM'
    assert events[0].get('end_time') == '11/01/2020 10:00 AM'
    assert events[1].get('name') == 'Lunch'
    assert events[1].get('start_time') == '11/01/2020 01:00 PM'
    assert events[1].get('end_time') == '11/01/2020 02:00 PM'
