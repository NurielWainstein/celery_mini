from sqlalchemy.orm import Session
from dbi.sql_connector import Base

class BaseModel(Base):
    __abstract__ = True  # Mark this as an abstract class

    @classmethod
    def create(cls, db: Session, **kwargs):
        instance = cls(**kwargs)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance

    @classmethod
    def get(cls, db: Session, **filters):
        return db.query(cls).filter_by(**filters).first()

    @classmethod
    def delete(cls, db: Session, instance):
        db.delete(instance)
        db.commit()

    @classmethod
    def update(cls, db: Session, instance, **kwargs):
        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        db.commit()
        db.refresh(instance)
        return instance

    @classmethod
    def get_all(cls, db: Session):
        return db.query(cls).all()

    @classmethod
    def get_by_filter(cls, db: Session, **filters):
        return db.query(cls).filter_by(**filters).all()
