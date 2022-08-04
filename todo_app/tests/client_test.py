import pymongo
import pytest
import os
import mongomock

from dotenv import load_dotenv, find_dotenv
from todo_app import app

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = app.create_app()
        with test_app.test_client() as client:
            yield client

def test_index_page(client):
    print(client.list_database_names())
    db_connection = pymongo.MongoClient(os.environ.get('MONGO_CONNECTION_STRING'))
    db = db_connection[os.environ.get('MONGO_DATABASE_NAME')]
    items = db.items
    new_item_name = "Test new item name"
    new_item = {
        "name": new_item_name,
        "status": "To Do"
    }
    items.insert_one(new_item)
    
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.data.decode('utf8')
    assert new_item_name in data