from datetime import datetime

from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from sqlalchemy.orm import Session

from config import EXCEL_EXTENSION
from dbi.elastic.elasticsearch_client import ElasticsearchClient
from dbi.models.category import Category
from dbi.utils import get_db
from storage.storage_handler import StorageHandler
from utils.documents.excel_processing import process_excel_on_upload
from typing import List

# Initialize the router
router = APIRouter()

elastic_search = ElasticsearchClient()
storage_handler = StorageHandler()


# Upload file endpoint
@router.post("/upload/{category_name}")
async def upload_file(category_name: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        file_name = file.filename

        if file_name.endswith(EXCEL_EXTENSION):
            # Check if category exists
            category = db.query(Category).filter(Category.name == category_name).first()
            if not category:
                raise HTTPException(status_code=404, detail="Category not found")

            # Save the uploaded file to disk
            file_path = storage_handler.upload_file_to_category(file, category_name)

            if file_path:
                # process xlsx data
                excel_text, numbers_sum = process_excel_on_upload(file_path)

                # save in elastic
                doc_id = elastic_search.insert_document(
                    doc_type=category.type,
                    region=category.region,
                    category=category_name,
                    created_at=datetime.now().isoformat(),
                    total_sum=numbers_sum,
                    doc_text=excel_text
                )

                # update category count
                count = category.count
                new_count = count+numbers_sum
                Category.update(db, category, count=count+numbers_sum)
                print(f"count of category {category_name} was updated to {new_count}")

                return {"message": f"File uploaded successfully at {file_path}, with id {doc_id}"}
            else:
                raise HTTPException(status_code=500, detail="could not save file in storage")
        else:
            raise HTTPException(status_code=400, detail="invalid file type, upload xlsx")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/find_regions")
async def find_regions(search_term: str, db: Session = Depends(get_db)):
    try:
        # Fetch unique regions from the categories
        existing_regions = Category.get_unique_regions(db)

        if not existing_regions:
            raise HTTPException(status_code=404, detail="No categories with regions found")

        # Query Elasticsearch to find documents that match the search term
        matching_regions = elastic_search.find_regions(search_term, existing_regions)

        if not matching_regions:
            raise HTTPException(status_code=404, detail="No regions found with the search term")

        # return dict incase that in the future we would like to change the response
        return {"matching_regions": matching_regions}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/sum_type")
async def sum_type(document_type: str, db: Session = Depends(get_db)):
    try:
        # Get the sum for the specified category type
        total_sum = Category.sum_count_by_type(db, document_type)

        if total_sum is None:
            raise HTTPException(status_code=404, detail=f"No sums found for type '{document_type}'")

        return {"total_sum": total_sum}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
