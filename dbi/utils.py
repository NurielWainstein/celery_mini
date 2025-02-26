from dbi.sql_connector import SessionLocal
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from functools import wraps


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# maybe use this in endpoints that need to use db connection? - further research code design with fastapi+sqlalchemy
def with_db(func):
    """Decorator to inject DB session into the route handler."""
    @wraps(func)
    def wrapper(*args, db: Session = Depends(get_db), **kwargs):
        try:
            return func(*args, db=db, **kwargs)
        except Exception as e:
            db.rollback()  # Rollback in case of an error
            raise HTTPException(status_code=400, detail=str(e))
    return wrapper
