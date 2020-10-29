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


def test_group_info(client):
    resp = client.get('/api/group/1/home')
    data = json.loads(resp.data)
    assert data.get('name') == 'Group A'
    assert data.get('welcome') == 'Welcome to Group A!'
