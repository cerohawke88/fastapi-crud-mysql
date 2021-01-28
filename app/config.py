from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import secrets

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root@localhost/fastapi_crud_practice"
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"

# 60 minutes * 24 hours * 7 days = 7 days
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

Base.metadata.create_all(bind=engine)