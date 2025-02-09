# app/main.py

from fastapi import FastAPI, Depends
from .routers.admin import admin_router
from .routers.creator import creator_router
from .routers.content import course_router
from .routers.user import user_router
from contextlib import asynccontextmanager
from .db import database


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not database.is_connected:
        await database.connect()
    yield


app = FastAPI(title="Insight Backend", lifespan=lifespan)


@app.get("/")
async def read_root():
    return {}


app.include_router(admin_router)
app.include_router(creator_router)
app.include_router(course_router)
app.include_router(user_router)
