from fastapi.testclient import TestClient

from my_project.main import app

client = TestClient(app=app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_item():
    response = client.post("/", headers={"x-token": "coneofsilence"}, json={"id": "foobar", "title": "Foo Bar", "description": "The Foo Barters"})

    assert response.status_code == 200
    assert response.json() == {"id": "foobar", "title": "Foo Bar", "description": "The Foo Barters"}

def test_by_id():
    response = client.get("/bar", headers={"x-token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == {"id": "bar", "title": "Bar", "description": "The bartenders"}