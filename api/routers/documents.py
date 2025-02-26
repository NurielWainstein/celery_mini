from datetime import datetime
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from sqlalchemy.orm import Session
import logging

from config import EXCEL_EXTENSION
from dbi.elastic.elasticsearch_client import ElasticsearchClient
from dbi.models.category import Category
from dbi.utils import get_db
from storage.storage_handler import StorageHandler
from utils.documents.excel_processing import process_excel_on_upload
from typing import Dict, Any

# Initialize the router
router = APIRouter()

elastic_search = ElasticsearchClient()
storage_handler = StorageHandler()

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# Helper function for file upload
async def handle_file_upload(file: UploadFile, category_name: str, db: Session) -> Dict[str, Any]:
    try:
        file_name = file.filename

        if not file_name.endswith(EXCEL_EXTENSION):
            raise HTTPException(status_code=400, detail="Invalid file type. Only .xlsx files are allowed.")

        # Check if category exists
        category = db.query(Category).filter(Category.name == category_name).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        # Save the uploaded file to disk
        file_path = storage_handler.upload_file_to_category(file, category_name)
        if not file_path:
            raise HTTPException(status_code=500, detail="Could not save file to storage")

        # Process Excel file
        excel_text, numbers_sum = process_excel_on_upload(file_path)

        # Insert into Elasticsearch
        doc_id = elastic_search.insert_document(
            doc_type=category.type,
            region=category.region,
            category=category_name,
            created_at=datetime.now().isoformat(),
            total_sum=numbers_sum,
            doc_text=excel_text
        )

        # Update category count in DB
        count = category.count
        new_count = count + numbers_sum
        Category.update(db, category, count=new_count)

        logger.info(f"Count for category {category_name} updated to {new_count}")

        return {"message": f"File uploaded successfully. Document ID: {doc_id}"}

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error during file upload: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/upload/{category_name}")
async def upload_file(category_name: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    return await handle_file_upload(file, category_name, db)


@router.get("/find_regions")
async def find_regions(search_term: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    try:
        existing_regions = Category.get_unique_regions(db)
        if not existing_regions:
            raise HTTPException(status_code=404, detail="No categories with regions found")

        matching_regions = elastic_search.find_regions(search_term, existing_regions)

        if not matching_regions:
            raise HTTPException(status_code=404, detail="No regions found with the search term")

        return {"matching_regions": matching_regions}

    except HTTPException as http_exc:
        logger.error(f"Error: {str(http_exc)}")
        raise http_exc
    except Exception as e:
        logger.error(f"Error in find_regions: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/sum_type")
async def sum_type(document_type: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    try:
        total_sum = Category.sum_count_by_type(db, document_type)

        if total_sum is None:
            raise HTTPException(status_code=404, detail=f"No sums found for type '{document_type}'")

        return {"total_sum": total_sum}

    except HTTPException as http_exc:
        logger.error(f"Error: {str(http_exc)}")
        raise http_exc
    except Exception as e:
        logger.error(f"Error in sum_type: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")