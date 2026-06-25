import jwt
import os

from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from App.database.database import get_db
from App.database import crud

# Key configurations
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

if SECRET_KEY is None:
    raise ValueError("SECRET_KEY is not set in the environment variables.")