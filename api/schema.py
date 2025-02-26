from pydantic import BaseModel

class CategoryCreate(BaseModel):
    category_name: str
    region: str
    type: str

class CategoryResponse(BaseModel):
    name: str
    region: str
    type: str

    class Config:
        orm_mode = True  # Allows the model to work seamlessly with SQLAlchemy models