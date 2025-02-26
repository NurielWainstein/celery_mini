from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:1234@localhost:5432/celery_db"

# Create the engine and session
engine = create_engine(DATABASE_URL, echo=True)

# Session maker to create session instances
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for the models to inherit from
Base = declarative_base()
