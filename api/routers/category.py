from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.schema import CategoryCreate, CategoryResponse
from dbi.models.category import Category
from dbi.utils import get_db

# Initialize the router
router = APIRouter()

@router.post("/create", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    try:
        new_category_data = {
            "name": category.category_name,
            "region": category.region,
            "type": category.type,
            "count": 0
        }
        new_category = Category.create(db, **new_category_data)

        return new_category
    except Exception as e:
        db.rollback()  # Rollback in case of an error
        raise HTTPException(status_code=400, detail=str(e))

