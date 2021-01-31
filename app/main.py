from fastapi import FastAPI, Query, Path, Body, Depends, Request, status
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from app import routers
from fastapi.security import OAuth2PasswordBearer
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI(title="FastAPI CRUD MySQL")

app.include_router(routers.users, prefix="/api")
app.include_router(routers.items, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Hello World!"}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )