from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, func, DateTime, and_, desc
from sqlalchemy.orm import relationship, Session
from app.config import Base
from app import schemas, models


class Item(Base):
    __tablename__ = "items"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(255), index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    user = relationship("User", back_populates="items")

    def save_to_db(db, item):
        db.add(item)
        db.commit()
        db.refresh(item)

    def get_item(db: Session, item_id: int):
        return db.query(Item).filter(Item.id == item_id).first()

    def get_items(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Item).offset(skip).limit(limit).all()

    def get_own_items(db: Session, user_id: int, skip: int = 0, limit: int = 100):
        return db.query(Item).filter(Item.user_id == user_id).offset(skip).limit(limit).all()

    def get_own_item(db: Session, item_id: int, user_id: int):
        return db.query(Item).filter(and_(Item.id == item_id, models.User.id == user_id)).first()

    def add_item(db: Session, item: schemas.ItemCreate, user_id: int):
        print(item)
        db_item = Item(
            **item.dict(),
            user_id = user_id
        )
        Item.save_to_db(db, db_item)
        return db_item.__dict__