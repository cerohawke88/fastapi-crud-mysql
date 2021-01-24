from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas, config, dependencies, auth

class ItemController:
    @staticmethod
    def create_item(
      item: schemas.ItemCreate, 
      db: Session = Depends(dependencies.get_db), 
      user: models.User = Depends(dependencies.get_current_user)
    ) -> Any:
      return models.Item.add_item(db, item=item, user_id=user.id)

    @staticmethod
    def read_items(db: Session = Depends(dependencies.get_db), skip: int = 0, limit: int = 100):
      # read all items
      items = models.Item.get_items(db, skip=skip, limit=limit)
      return items

    @staticmethod
    def read_own_items(
      db: Session = Depends(dependencies.get_db), 
      user: models.User = Depends(dependencies.get_current_user), 
      skip: int = 0, limit: int = 100
    ):
      # read all own items
      items = models.Item.get_own_items(db, user_id = user.id, skip=skip, limit=limit)
      return items

    @staticmethod
    def read_item(item_id: int, db: Session = Depends(dependencies.get_db)):
      # read one specific item
      item = models.Item.get_item(db, item_id=item_id)
      if item is None:
          raise HTTPException(status_code=404, detail="Item not found")
      return item

    @staticmethod
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
      return item
    