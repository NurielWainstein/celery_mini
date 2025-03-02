import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
STORAGE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "storage")
UPLOAD_FOLDER = os.path.join(STORAGE_PATH, "uploads")

EXCEL_EXTENSION = ".xlsx"

ELASTIC_HOST = os.getenv("ELASTIC_HOST", "http://localhost:9200")
LOCAL_ELASTIC_HOST = os.getenv("LOCAL_ELASTIC_HOST", "http://localhost:9200")

DATABASE_SQL_URL = os.getenv("SQL_URL")
SQL_HOST_NAME=os.getenv("SQL_HOST_NAME")
SQL_PORT=os.getenv("SQL_PORT")
SQL_DBNAME=os.getenv("SQL_DBNAME")
SQL_USER=os.getenv("SQL_USER")
SQL_PASSWORD=os.getenv("SQL_PASSWORD")


# regex
FLOAT_NUMBER_REG=r'-?\d+\.\d+|-?\d+'