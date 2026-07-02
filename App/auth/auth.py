import jwt
import os

from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database import crud

# Key configurations
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

if SECRET_KEY is None:
    raise ValueError("SECRET_KEY is not set in the environment variables.")

# Create an access token
def create_access_token(user_name: str):
    # Create a JWT token with the user's username and expiration time
    payload = {
        "action": "login",
        "sub": user_name,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# Get the current user from the token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Decode the JWT token and extract the username
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_name: str | None = payload.get("sub") 
        
        # Check if the username is present in the token payload
        if user_name is None:
            raise HTTPException(status_code=401, detail="Invalid token: missing subject.")
    
    # Handle token errors
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")

    # Retrieve the user from the database using the extracted username
    user = crud.get_user_by_username(db, user_name)
    
    # Check if the user exists in the database
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    
    return user