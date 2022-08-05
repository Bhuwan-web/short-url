from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import database

from .routers import short_url

get_db = database.get_db


app = FastAPI()
origins = [
    # "*",
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(short_url.router)


@app.get("/")
def home():
    return {"home": "Hello World"}
