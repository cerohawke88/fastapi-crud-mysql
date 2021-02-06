from datetime import timedelta
from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas, config, dependencies, auth

items = APIRouter(prefix="/items", tags=["items"])

@items.post("/", response_model=schemas.ItemCreate)
def create_item(
  item: schemas.ItemCreate, 
  db: Session = Depends(dependencies.get_db), 
  user: models.User = Depends(dependencies.get_current_user)
) -> Any:
  return models.Item.add_item(db, item=item, user_id=user.id)


@items.get("/", response_model=schemas.ItemResponse[List[schemas.Item]])
def read_items(db: Session = Depends(dependencies.get_db), skip: int = 0, limit: int = 100):
  # read all items
  items = models.Item.get_items(db, skip=skip, limit=limit)
  return {
    "message": "success",
    "data": items
  }


@items.get("/me", response_model=schemas.ItemResponse[List[schemas.Item]])
def read_own_items(
  db: Session = Depends(dependencies.get_db), 
  user: models.User = Depends(dependencies.get_current_user), 
  skip: int = 0, limit: int = 100
):
  # read all own items
  items = models.Item.get_own_items(db, user_id = user.id, skip=skip, limit=limit)
  return {
    "message": "success",
    "data": items
  }


@items.get("/{item_id}", response_model=schemas.ItemResponse[schemas.Item])
def read_item(item_id: int, db: Session = Depends(dependencies.get_db)):
  # read one specific item
  item = models.Item.get_item(db, item_id=item_id)
  if item is None:
      raise HTTPException(status_code=404, detail="Item not found")
  return {
    "message": "success",
    "data": items
  }


@items.get("/me/{item_id}", response_model=schemas.ItemResponse[schemas.Item])
def read_own_item(
  item_id: int,
  user: models.User = Depends(dependencies.get_current_user), 
  skip: int = 0, limit: int = 100,
  db: Session = Depends(dependencies.get_db), 
):
  # read one own specific item
  item = models.Item.get_own_item(db, item_id=item_id, user_id = user.id)
  if item is None:
    return HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Unauthorized. Item is not yours.",
    )
  return {
    "message": "success",
    "data": items
  }
