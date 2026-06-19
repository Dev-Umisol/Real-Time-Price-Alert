from fastapi import HTTPException
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from . import models, schemas

# CRUD Operations for Users
def create_user(db: Session, user: schemas.UserRegistration) -> models.Users:
    # Hash the user's password
    password_hash = PasswordHash.recommended()
    hashed_password = password_hash.hash(user.user_password)
    
    # Create a new user instance and save it to the database
    db_user = models.Users(user_name = user.user_name, user_password = hashed_password)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user