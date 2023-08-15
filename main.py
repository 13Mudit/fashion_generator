from fastapi import FastAPI
from pydantic import BaseModel


class Query(BaseModel):
    user: str
    query: str


app = FastAPI()


@app.post("/query/")
async def generate(query: Query):
    return query


@app.get("/image/")
async def get_image():
    return None