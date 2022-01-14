import pytest
import os
import requests

from dotenv import load_dotenv, find_dotenv
from todo_app import app

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    
    # Create the new app.
    test_app = app.create_app()
    
    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client

def test_index_page(monkeypatch, client):
    # Replace call to requests.get(url) with our own function
    monkeypatch.setattr(requests, 'get', get_stubs)

    response = client.get('/')

class StubResponse():
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data

    def json(self):
        return self.fake_response_data

def get_stubs(url, params):
    test_board_name = os.environ.get('TRELLO_DEFAULT_BOARD_NAME')
    test_board_id = os.environ.get('TRELLO_DEFAULT_BOARD_ID')
    fake_response_data = None
    if url == f'https://api.trello.com/1/boards/{test_board_id}/lists':
        fake_response_data = [{
            'id': test_board_id,
            'name': test_board_name,
            'cards': [{'id': '456', 'name': 'Test card'}]
        }]
    if url == f'https://api.trello.com/1/members/me/boards':
        fake_response_data = [{
            'name': test_board_name,
            'id': test_board_id
        }]
    return StubResponse(fake_response_data)