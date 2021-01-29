from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, func, DateTime
from sqlalchemy.orm import Session, relationship
from app.config import Base
from app import schemas
from app.auth import get_password_hash, verify_password

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    email = Column(String(120), unique=True, index=True)
    password = Column(String(255))
    photo = Column(String(120), index=True, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    items = relationship("Item", back_populates="user")

    def save_to_db(db, item):
        db.add(item)
        db.commit()
        db.refresh(item)

    def get_user(db: Session, id: int):
        return db.query(User).filter(User.id == id).first()


    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()


    def get_users(db: Session, skip: int = 0, limit: int = 100):
        return db.query(User).offset(skip).limit(limit).all()

    def authenticate_user(db: Session, email: str, password: str):
        user = User.get_user_by_email(db, email)
        if not user:
            return False
        if not verify_password(password, user.password):
            return False
        return user

    def create_user(db: Session, user: schemas.UserCreate):
        db_user = User(
            name = user.name,
            email = user.email, 
            password = get_password_hash(user.password)
        )
        print(db_user)
        User.save_to_db(db, db_user)
        return db_user.__dict__