from datetime import datetime, timezone
from fastapi.testclient import TestClient


from my_project.main import app


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_get_all_product():
    response = client.get("/product/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    product = data[0]
    assert "id" in product
    assert "name" in product
    assert "price" in product
    assert "category" in product

    assert isinstance(product["id"], str)
    assert isinstance(product["name"], str)
    assert isinstance(product["price"], str)
    assert isinstance(product["category"], dict)


def test_create_product():
    data_product = {
        "name": "мандарин1",
        "price": 11,
        "category": {"name": "фрукт"},
    }
    response = client.post("/product/", json=data_product)
    assert response.status_code == 201


def test_update_product():
    id_product = "41d5c0f3-d876-42d7-9c13-afe50a44828b"
    now = datetime.now(timezone.utc)
    data_update = {
        "name": "мандарин большой",
        "price": 44,
        "category": {"name": "фрукт"},
        "create_at": now.isoformat(),
    }
    response = client.patch(f"/product/{id_product}/", json=data_update)
    assert response.status_code == 200

    json_response = response.json()

    assert json_response["name"] == "мандарин большой"
    assert json_response["price"] == "44.00"
    assert json_response["category"]["name"] == "фрукт"
