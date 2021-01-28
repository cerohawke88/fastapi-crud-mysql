from fastapi import FastAPI, Query, Path, Body, Depends
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from app import routers

app = FastAPI(title="FastAPI CRUD MySQL")

app.include_router(routers.users, prefix="/api")
app.include_router(routers.items, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Hello World!"}