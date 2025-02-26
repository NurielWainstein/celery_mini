import os
import logging
from config import UPLOAD_FOLDER

# Set up logging
logging.basicConfig(level=logging.INFO)  # You can change the level to DEBUG, WARNING, etc.
logger = logging.getLogger(__name__)

class StorageHandler:
    def __init__(self):
        self.base_upload_path = UPLOAD_FOLDER

    def read_file(self, file_path: str):
        """Reads the contents of a file."""
        try:
            with open(file_path, "rb") as file:
                return file.read()
        except Exception as e:
            logger.error(f"Could not read file: {e}")
            return None

    def save_file(self, file, file_name, destination: str):
        try:
            file_path = os.path.join(destination, file_name)
            with open(file_path, "wb") as buffer:
                buffer.write(file.file.read())
            logger.info(f"File saved successfully at {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"Could not save file: {e}")
        return None

    def upload_file_to_category(self, file, category_name):
        upload_category_path = os.path.join(self.base_upload_path, category_name)
        os.makedirs(upload_category_path, exist_ok=True)

        saved_path = self.save_file(file, file.filename, upload_category_path)

        if saved_path:
            logger.info(f"File uploaded to category {category_name} at {saved_path}")
        else:
            logger.error(f"Failed to upload file to category {category_name}")

        return saved_path
