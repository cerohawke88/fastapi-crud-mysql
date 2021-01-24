from fastapi import APIRouter
from typing import List

from app.controllers.User import UserController
from app.controllers.Item import ItemController
from app import schemas

users = APIRouter(prefix="/users", tags=["users"])
items = APIRouter(prefix="/items", tags=["items"])

# =============================== Users ===============================
@users.post("/login", response_model=schemas.Token)
async def action():
    return await UserController.login()

@users.post("/register", response_model=schemas.UserCreate)
async def action():
    return await UserController.register()

@users.get("/", response_model=List[schemas.User])
async def action():
    return await UserController.read_users()

@users.get("/{user_id}", response_model=schemas.User)
async def action(user_id: int):
    return await UserController.read_user(user_id)

@users.get("/profile", response_model=schemas.User)
async def action():
    return await UserController.read_profile()

# =============================== Items ===============================
@items.post("/", response_model=schemas.ItemCreate)
async def action():
    return await ItemController.create_item()

@items.get("/", response_model=List[schemas.Item])
async def action():
    return await ItemController.read_items()

@items.get("/me", response_model=List[schemas.Item])
async def action():
    return await ItemController.read_own_items()

@items.get("/{item_id}", response_model=schemas.Item)
async def action(item_id: int):
    return await ItemController.read_item(item_id)

@items.get("/me/{item_id}", response_model=schemas.Item)
async def action(item_id: int):
    return await ItemController.read_own_item(item_id)