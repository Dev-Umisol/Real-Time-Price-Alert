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

# Celery task to check cryptocurrency prices and notify users if the price exceeds their set limit.
@celery_app.task
def check_crypto_prices():
    """
    Celery task to check cryptocurrency prices and notify users if the price exceeds their set limit.
    """
    with Session(engine) as session:
        active_alerts = crud.get_all_active_alerts(session)

        for alert in active_alerts:
            current_coin_price = get_coin_price(alert.coin_name)
            
            if current_coin_price is not None and current_coin_price <= alert.coin_price_threshold:
                # Notify the user via WebSocket
                connection_manager = connections.ConnectionManager()