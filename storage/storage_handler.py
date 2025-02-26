import os

from config import UPLOAD_FOLDER


class StorageHandler:
    def __init__(self):
        self.base_upload_path = UPLOAD_FOLDER


    def read_file(self, file_path: str):
        """Reads the contents of a file."""
        try:
            with open(file_path, "rb") as file:
                return file.read()
        except Exception as e:
            print(f"Could not read file: {e}")
            return None

    def save_file(self, file, file_name, destination: str):
        try:
            file_path = os.path.join(destination, file_name)
            with open(file_path, "wb") as buffer:
                buffer.write(file.file.read())
            return file_path
        except Exception as e:
            print(f"Could not save file: {e}")
        return None

    def upload_file_to_category(self, file, category_name):
        upload_category_path = os.path.join(self.base_upload_path, category_name)
        os.makedirs(upload_category_path, exist_ok=True)

        saved_path = self.save_file(file, file.filename, upload_category_path)

        return saved_path
