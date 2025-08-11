import uvicorn
from typing import Annotated
from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel

app = FastAPI()
fake_secret_token = "coneofsilence"

fake_db = {
    "foo": {"id": "foo", "title": "Foo", "description": "There goes my hero"},
    "bar": {"id": "bar", "title": "Bar", "description": "The bartenders"},
}

class Item(BaseModel):
    id: str
    title: str
    description: str | None = None


@app.get("/")
async def get_hello():
    return {"message": "Hello World"}

@app.post("/")
async def post_create(item: Item, x_token: Annotated[str, Header()]):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid X-Token header")
    if item.id in fake_db:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Item already exists")
    fake_db[item.id] = item
    return item

@app.get("/{id}")
async def get_by_id(id: str, x_token: Annotated[str, Header()]):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid X-Token header")
    if id not in fake_db:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Item already exists")
    return fake_db[id]

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)