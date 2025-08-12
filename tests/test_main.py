import pytest
from fastapi.testclient import TestClient

from my_project.main import app, fake_db

client = TestClient(app=app)

@pytest.fixture
def data_example():
    return {"id": "bar", "title": "Bar", "description": "The bartenders"}

@pytest.fixture(autouse=True)
def fake_db_clear():
    fake_db.clear()
    return fake_db

@pytest.fixture
def add_db(data_example):
    fake_db[data_example["id"]] = data_example
    return fake_db

@pytest.fixture
def token_header():
    return {"x-token": "coneofsilence"}


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_item(data_example, token_header):
    response = client.post("/", headers=token_header, json=data_example)

    assert response.status_code == 200
    assert response.json() == data_example

def test_by_id(data_example, add_db, token_header):
    response = client.get("/bar", headers=token_header)
    assert response.status_code == 200
    assert response.json() == data_example