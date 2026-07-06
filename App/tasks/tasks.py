import os

from celery import Celery
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from app.database import crud
from app.database.database import engine
from app.services.coingecko import get_coin_price
from app.websocket import connections

# Load environment variables from .env file
load_dotenv()
REDIS_URL = os.getenv("REDIS_URL")

# Safety check for REDIS_URL
if not REDIS_URL:
    raise ValueError("Environment variable 'REDIS_URL' is not set")

# Create Celery app instance
celery_app = Celery(
    "tasks",
    broker=REDIS_URL,
    backend=REDIS_URL
)