from celery import Celery
from sqlalchemy.orm import Session

from app.database import crud
from app.database.database import engine
from app.services.coingecko import get_coin_price
from app.websocket import connections

