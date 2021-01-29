from datetime import timedelta
from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import models, schemas, config, dependencies, auth

users = APIRouter(prefix="/users", tags=["users"])

@users.post("/login", response_model=schemas.Token)
def login(
  db: Session = Depends(dependencies.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
  """
  OAuth2 compatible token login, get an access token for future requests
  """
  user = models.User.authenticate_user(
      db, email=form_data.username, password=form_data.password
  )
  if not user:
      raise HTTPException(status_code=400, detail="Incorrect email or password")
  access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = auth.create_access_token(
        data={"sub": user.id, "email": user.email}, expires_delta=access_token_expires
  )
  return {
      "access_token": access_token,
      "token_type": "Bearer",
  }

@users.post("/register", response_model=schemas.UserCreate)
def register(
  *,
  db: Session = Depends(dependencies.get_db),
  user: schemas.UserCreate,
) -> Any:
  """
  Create new user.
  """
  db_user = models.User.get_user_by_email(db, email=user.email)
  print(db_user)
  if db_user:
      raise HTTPException(
        status_code=400,
        detail="Email already registered.",
      )
  reg_user = models.User.create_user(db, user=user)
  return reg_user

@users.get("/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)):
  """
  Read all users
  """
  users = models.User.get_users(db=db, skip=skip, limit=limit)
  return users

@users.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(dependencies.get_db)):
  """
  Read one specific user
  """
  db_user = models.User.get_user(db, user_id)
  if db_user is None:
      raise HTTPException(status_code=404, detail="User not found")
  return db_user

@users.get("/profile", response_model=schemas.User)
def read_profile(user: models.User = Depends(dependencies.get_current_user), db: Session = Depends(dependencies.get_db)):
  """
  Read current logged in user as a profile
  """
  return user