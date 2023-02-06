import pytest

from server import create_app


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, email='club_one@test.com'):
        return self._client.post('/showSummary', data={'email': email})

    def logout(self):
        return self._client.get('/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
