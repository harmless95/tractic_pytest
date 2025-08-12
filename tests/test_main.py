import pytest
from fastapi.testclient import TestClient

from my_project import fake_db
from my_project.main import app

client = TestClient(app=app)


@pytest.fixture
def data_example():
    return {"id": "bar", "title": "Bar", "description": "The bartenders"}


@pytest.fixture(autouse=True)
def fake_db_clear():
    fake_db.clear()
    yield


@pytest.fixture
def add_db():
    fake_db.update(
        {
            "foo": {"id": "foo", "title": "Foo", "description": "There goes my hero"},
            "bar": {"id": "bar", "title": "Bar", "description": "The bartenders"},
        }
    )
    return fake_db


@pytest.fixture
def token_header():
    return {"x-token": "coneofsilence"}


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


class TestItem:

    def test_create_item(self, data_example, token_header):
        response = client.post("/item/", headers=token_header, json=data_example)

        assert response.status_code == 200
        assert response.json() == data_example

    @pytest.mark.parametrize(
        "url, data",
        [
            (
                "/item/bar/",
                {"id": "bar", "title": "Bar", "description": "The bartenders"},
            ),
            (
                "/item/foo/",
                {"id": "foo", "title": "Foo", "description": "There goes my hero"},
            ),
        ],
    )
    def test_by_id(self, add_db, token_header, url, data):
        response = client.get(url, headers=token_header)
        assert response.status_code == 200
        assert response.json() == data
