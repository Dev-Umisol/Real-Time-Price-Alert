import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Safety check for DATABASE_URL
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the environment variables.")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base Class for Declarative Models
class Base(DeclarativeBase):
    pass

# Dependency to get DB Session
def get_db():
    db = SessionLocal()
    
    try:
        yield db # Yield the database session to be used in the application
    finally:
        db.close() # Ensure the database session is closed after use