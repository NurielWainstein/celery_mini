from sqlalchemy import Column, String, Integer, func

from dbi.models.base import BaseModel
from sqlalchemy.orm import Session

class Category(BaseModel):
    __tablename__ = 'categories'

    name = Column(String, primary_key=True)
    region = Column(String, nullable=False)
    type = Column(String, nullable=False)
    count = Column(Integer, nullable=False)

    @classmethod
    def sum_count_by_type(cls, db: Session, category_type: str):
        total_count = db.query(func.sum(cls.count)) \
                        .filter(cls.type == category_type) \
                        .scalar()
        return total_count

    @classmethod
    def get_unique_regions(cls, db: Session):
        return [region[0] for region in db.query(cls.region).distinct().all()]

