from sqlalchemy import Column, String
from dbi.sql_connector import Base
from sqlalchemy.orm import Session

class Category(Base):
    __tablename__ = 'categories'

    name = Column(String, primary_key=True)
    region = Column(String, nullable=False)
    type = Column(String, nullable=False)

    @classmethod
    def create(cls, db: Session, name: str, region: str, type: str):
        db_category = cls(name=name, region=region, type=type)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category

    @classmethod
    def get_by_id(cls, db: Session, category_id: str):
        return db.query(cls).filter(cls.id == category_id).first()

    @classmethod
    def delete(cls, db: Session, category: 'Category'):
        db.delete(category)
        db.commit()
