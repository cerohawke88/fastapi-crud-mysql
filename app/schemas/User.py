from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel, EmailStr
from app.schemas import Item
from pydantic.generics import GenericModel

# Creates a generic type
UserGeneric = TypeVar('UserGeneric')

# Base Shared properties
class UserBase(BaseModel):
  name: str
  email: EmailStr
  photo: Optional[str] = None

# Properties to receive via API on create
class UserCreate(UserBase):
  password: str

# Properties to receive via API on update
class UserUpdate(UserBase):
  password: Optional[str] = None
  
# Properties to receive via API on read
class User(UserBase):
  id: int
  items: List[Item] = []

  class Config:
    orm_mode = True

class UserResponse(GenericModel, Generic[UserGeneric]):
  message: str
  data: UserGeneric