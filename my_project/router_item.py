from typing import Annotated
from fastapi import APIRouter, HTTPException, Header, status
from pydantic import BaseModel


router = APIRouter(prefix="/item", tags=["Item"])

fake_secret_token = "coneofsilence"

fake_db = {
    "foo": {"id": "foo", "title": "Foo", "description": "There goes my hero"},
    "bar": {"id": "bar", "title": "Bar", "description": "The bartenders"},
}


class Item(BaseModel):
    id: str
    title: str
    description: str | None = None


@router.post("/")
async def post_create(item: Item, x_token: Annotated[str, Header()]):
    if x_token != fake_secret_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid X-Token header"
        )
    if item.id in fake_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Item already exists"
        )
    fake_db[item.id] = item.model_dump()
    return fake_db[item.id]


@router.get("/{id}/")
async def get_by_id(id: str, x_token: Annotated[str, Header()]):
    if x_token != fake_secret_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid X-Token header"
        )
    if id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Item already exists"
        )
    return fake_db[id]
