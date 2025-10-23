import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from core.config import setting
from core.model import db_helpers
from my_project.api.routers import all_routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    finally:
        await db_helpers.dispose()


app = FastAPI()
app.include_router(router=all_routers)


@app.get("/")
async def get_hello():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=setting.run.host,
        port=setting.run.port,
    )
