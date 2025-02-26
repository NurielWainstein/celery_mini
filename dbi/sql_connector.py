from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import DATABASE_SQL_URL

# Create the engine and session
engine = create_engine(DATABASE_SQL_URL, echo=True)

# Session maker to create session instances
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for the models to inherit from
Base = declarative_base()
