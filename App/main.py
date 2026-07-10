from fastapi import FastAPI, Depends, HTTPException, WebSocket

from app.auth import auth
from app.database import crud, schemas, models
from app.database.database import get_db, engine
from app.websocket.connections import connection_manager

# Create FastAPI app instance
app = FastAPI(title="Real Time Crypto Price Alert")

# Create database tables
models.Base.metadata.create_all(bind=engine)

# User registration endpoint
@app.post('/users/register', response_model=schemas.UserResponse, status_code=201)
def register_user(user: schemas.UserRegistration, db=Depends(get_db)):
    """
    Register a new user
    """
    # Check if the username already exists in the database
    if crud.get_user_by_username(db, user.user_name):
        raise HTTPException(status_code=409, detail="Username already exists")
    
    new_user = crud.create_user(db, user) # Create a new user in the database using the provided user registration data
    
    return new_user