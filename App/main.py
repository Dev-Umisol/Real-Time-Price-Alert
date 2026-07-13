from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.security import OAuth2PasswordRequestForm
from pwdlib import PasswordHash

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

# User login endpoint
@app.post('/users/login', response_model=schemas.UserToken)
def user_login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    """
    User login endpoint
    """
    password_hash = PasswordHash.recommended()
    db_user = crud.get_user_by_username(db, form_data.username) # Retrieve the user's password from the database using the provided username
    
    if db_user is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Verify the provided password against the stored hashed password
    is_valid = password_hash.verify(form_data.password, db_user.user_password) # type: ignore
    
    if not is_valid:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    return {"access_token": auth.create_access_token(db_user.user_name), "token_type": "bearer"} # type: ignore

# Alert creation endpoint
@app.post('/alerts', response_model=schemas.UserAlertResponse, status_code=201)
def create_alert(alert: schemas.UserCreateAlert, db=Depends(get_db), current_user=Depends(auth.get_current_user)):
    """
    Create a new alert for the current user
    """
    new_alert = crud.create_new_alert(db, current_user.id, alert) # Create a new alert in the database for the current user
    
    return new_alert

# Alert retrieval endpoint
@app.get('/alerts/{id}', response_model=schemas.UserAlertResponse)
def get_alert(id: int, db=Depends(get_db), current_user=Depends(auth.get_current_user)):
    """
    Get a specific alert by ID for the current user
    """
    alert = crud.get_alert_by_id(db, id) # Retrieve the alert from the database using the provided ID
    
    if alert is None or alert.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied") # Raise an error if the alert does not exist or does not belong to the current user
    
    return alert

# Alert deletion endpoint
@app.delete('/alerts/{id}')
def delete_alert(id: int, db=Depends(get_db), current_user=Depends(auth.get_current_user)):
    """
    Delete a specific alert by ID for the current user
    """
    alert = crud.get_alert_by_id(db, id) # Retrieve the alert from the database using the provided ID
    
    if alert is None or alert.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied") # Raise an error if the alert does not exist or does not belong to the current user
    
    crud.delete_alert(db, id) # Delete the alert from the database
    
    return {"detail": "Alert deleted successfully"}

# WebSocket endpoint for real-time notifications
@app.websocket('/ws/{user_id}')
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """
    WebSocket endpoint for real-time notifications
    """
    await connection_manager.connect(websocket, user_id) # Connect the WebSocket and store it in the connection manager
    
    try:
        while True:
            data = await websocket.receive_text() # Wait for incoming messages from the WebSocket
            await websocket.send_text(f"Message received: {data}") # Echo the received message back to the client
    except WebSocketDisconnect:
        connection_manager.disconnect(user_id) # Disconnect the WebSocket and remove it from the connection manager when the client disconnects