import openpyxl

from storage.storage_handler import StorageHandler


def load_excel(file_path):
    try:
        storage_handler = StorageHandler()
        file_content = storage_handler.read_file(file_path)

        if file_content is None:
            return None

        # Load the Excel file from the byte content
        wb = openpyxl.load_workbook(filename=openpyxl.BytesIO(file_content))
        # You can add logic to process the data here if needed
        # For example, print the sheet names or do something with the contents
        sheet = wb.active
        rows = list(sheet.iter_rows(values_only=True))
        return rows
    except Exception as e:
        print(f"Could not process XLSX file: {e}")
        return None