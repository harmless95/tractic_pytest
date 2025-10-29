import pytest
import httpx
import pytest_asyncio
import os

from dotenv import load_dotenv
from datetime import datetime, timezone
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from core.model import Base
from my_project.main import app

dotenv_path = os.path.join(os.path.dirname(__file__), "..", "my_project", ".env")
load_dotenv(dotenv_path)
DATABASE_URL = os.getenv("APP_CONFIG__DB__URL")

engine = create_async_engine(url=DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)


@pytest_asyncio.fixture
async def db_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        async with session.begin():
            yield session
        await session.rollback()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest_asyncio.fixture
async def create_product(async_client):
    data_product = {
        "name": "мандарин 22",
        "price": 43,
        "category": {"name": "фрукт"},
    }
    response = await async_client.post("/product/", json=data_product)
    assert response.status_code == 201
    id_product = response.json()["id"]
    yield id_product
    await async_client.delete(f"/product/{id_product}/")


@pytest.mark.anyio
async def test_read_main(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@pytest.mark.anyio
async def test_get_all_product(async_client):
    response = await async_client.get("/product/")
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


@pytest.mark.anyio
async def test_update_product(async_client, create_product):
    now = datetime.now(timezone.utc)
    data_update = {
        "name": "мандарин большой",
        "price": 44,
        "category": {"name": "фрукт"},
        "create_at": now.isoformat(),
    }
    response = await async_client.patch(f"/product/{create_product}/", json=data_update)
    assert response.status_code == 200

    json_response = response.json()

    assert json_response["name"] == "мандарин большой"
    assert json_response["price"] == "44.00"
    assert json_response["category"]["name"] == "фрукт"


@pytest.mark.anyio
async def test_delete_product(async_client, create_product):
    response = await async_client.delete(f"/product/{create_product}/")
    assert response.status_code == 204

    check_product = await async_client.get(f"/product/{create_product}/")
    assert check_product.status_code == 404
