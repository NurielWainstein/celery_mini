from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from sqlalchemy.orm import Session

from dbi.elastic.elasticsearch_client import ElasticsearchClient
from dbi.models.category import Category
from dbi.utils import get_db
from storage.storage_handler import StorageHandler

# Initialize the router
router = APIRouter()

elastic_search = ElasticsearchClient()
storage_handler = StorageHandler()


# Upload file endpoint
@router.post("/upload/{category_name}")
async def upload_file(category_name: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Check if category exists
        category = db.query(Category).filter(Category.name == category_name).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        # Save the uploaded file to disk
        file_path = storage_handler.upload_file_to_category(file, category.name)

        # process xlsx data
        # extract numeric data

        # save in elastic

        if file_path:
            return {"message": f"File uploaded successfully at {file_path}"}
        else:
            raise HTTPException(status_code=500, detail="could not save file in storage")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
