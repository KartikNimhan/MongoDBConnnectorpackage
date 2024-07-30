import pytest
from mongodb_connect.mongo_crud import MongoOperation

@pytest.fixture
def mongo_op():
    return MongoOperation(client_url="mongodb://localhost:27017", database_name="test_db", collection_name="test_collection")

def test_create_mongo_client(mongo_op):
    client = mongo_op.create_mongo_client()
    assert client is not None

def test_create_database(mongo_op):
    db = mongo_op.create_database()
    assert db.name == "test_db"

def test_create_collection(mongo_op):
    collection = mongo_op.create_collection()
    assert collection.name == "test_collection"
