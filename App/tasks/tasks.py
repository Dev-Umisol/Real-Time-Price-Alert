import os
import asyncio

from celery import Celery, schedules
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from app.database import crud
from app.database.database import engine
from app.services.coingecko import get_coin_price
from app.websocket.connections import connection_manager

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

# Configure Celery beat schedule to run the check_crypto_prices task every minute
celery_app.conf.beat_schedule = {
    "check-crypto-prices-every-minute": {
        "task": "app.tasks.tasks.check_crypto_prices",
        "schedule": 60,  # Run every minute
    },
}

# Celery task to check cryptocurrency prices and notify users if the price exceeds their set limit.
@celery_app.task
def check_crypto_prices():
    """
    Celery task to check cryptocurrency prices and notify users if the price exceeds their set limit.
    """
    with Session(engine) as session:
        active_alerts = crud.get_all_active_alerts(session)

        # Loop through each active alert and check the current price of the specified cryptocurrency.
        for alert in active_alerts:
            current_coin_price = get_coin_price(alert.coin_name) # type: ignore
            
            # If the current price is less than or equal to the user's set threshold, send a notification and mark the alert as fired.
            if current_coin_price is not None and current_coin_price <= alert.coin_price_threshold: # type: ignore
                # Notify the user via WebSocket
                asyncio.run(connection_manager.send_notification(alert.user_id, f"Price alert: {alert.coin_name} has reached ${current_coin_price}.")) # type: ignore
                crud.update_alert_fired(session, alert.alert_id) # type: ignore

