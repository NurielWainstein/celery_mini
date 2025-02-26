from sqlalchemy.orm import Session
from dbi.sql_connector import SessionLocal
from dbi.models.category import Category

def create_and_delete_document():
    # Open a session
    db: Session = SessionLocal()

    try:
        # Create a new document
        new_document = Category.create(db, id="doc_1", category_id="cat_1", total_sum=500.0)
        print(f"Created document: {new_document}")

        # Query the document
        document = Category.get_by_id(db, document_id="doc_1")
        print(f"Document: {document}")

        # Delete the document
        if document:
            Category.delete(db, document)
            print(f"Deleted document: {document}")

    finally:
        # Close the session after all operations
        db.close()

# Run the example
create_and_delete_document()
