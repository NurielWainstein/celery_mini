from sqlalchemy import Column, String, Integer, func
from dbi.sql_connector import Base
from sqlalchemy.orm import Session

class Category(Base):
    __tablename__ = 'categories'

    name = Column(String, primary_key=True)
    region = Column(String, nullable=False)
    type = Column(String, nullable=False)
    count = Column(Integer, nullable=False)

    @classmethod
    def create(cls, db: Session, name: str, region: str, type: str, count: int):
        db_category = cls(name=name, region=region, type=type, count=count)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category

    @classmethod
    def get_by_name(cls, db: Session, category_name: str):
        return db.query(cls).filter(cls.name == category_name).first()

    @classmethod
    def delete(cls, db: Session, category: 'Category'):
        db.delete(category)
        db.commit()

    @classmethod
    def get_unique_regions(cls, db: Session):
        return [region[0] for region in db.query(cls.region).distinct().all()]

    @classmethod
    def update(cls, db: Session, category_name: str, **kwargs):
        # Fetch the category by name
        category = db.query(cls).filter(cls.name == category_name).first()

        if not category:
            return None  # or raise an exception if preferred

        # Update fields with the provided kwargs
        for key, value in kwargs.items():
            if hasattr(category, key):
                setattr(category, key, value)

        db.commit()  # Commit changes
        db.refresh(category)  # Refresh the category object to reflect changes
        return category

    @classmethod
    def sum_count_by_type(cls, db: Session, category_type: str):
        # Sum the 'count' for the given 'type'
        total_count = db.query(func.sum(cls.count)) \
                        .filter(cls.type == category_type) \
                        .scalar()
        return total_count