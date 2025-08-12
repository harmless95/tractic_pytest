import uvicorn
from fastapi import FastAPI


from router_item import router as router_item

app = FastAPI()
app.include_router(router=router_item)


@app.get("/")
async def get_hello():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
