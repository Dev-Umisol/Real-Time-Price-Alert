from fastapi import FastAPI, Depends, HTTPException, WebSocket

from app.auth import auth
from app.database import crud, schemas, models
from app.database.database import get_db, engine
from app.websocket.connections import connection_manager

# Create FastAPI app instance
app = FastAPI(title="Real Time Crypto Price Alert")

# Create database tables
models.Base.metadata.create_all(bind=engine)