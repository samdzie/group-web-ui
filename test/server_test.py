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
