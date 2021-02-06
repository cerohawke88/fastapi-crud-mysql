from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel
from pydantic.generics import GenericModel

# Creates a generic type
ItemGeneric = TypeVar('ItemGeneric')

class ItemBase(BaseModel):
  name: str
  description: Optional[str] = None

class ItemCreate(ItemBase):
  pass

class Item(ItemBase):
  id: int
  user_id: int

  class Config:
    orm_mode = True

class ItemResponse(GenericModel, Generic[ItemGeneric]):
  message: str
  data: ItemGeneric