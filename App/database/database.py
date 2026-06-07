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

