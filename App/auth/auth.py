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
    payload = {
        "action": "login",
        "sub": user_name,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)