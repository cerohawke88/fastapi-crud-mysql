from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root@localhost/fastapi_crud_practice"
# openssl rand -hex 32
SECRET_KEY = "b6b06f53cb2f8d1b0f57d077f8cbb979d6be911324a8d3ec334d01558a0f5ae8"
ALGORITHM = "HS256"

# 60 minutes * 24 hours * 7 days = 7 days
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

Base.metadata.create_all(bind=engine)