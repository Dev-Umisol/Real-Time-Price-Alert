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

# Retrieve a user by their username
def get_user_by_username(db: Session, user_name: str) -> models.Users | None:
    return db.query(models.Users).filter(models.Users.user_name == user_name).first()

# CRUD Operations for Alerts
def create_new_alert(db: Session, user_id: int, alert: schemas.UserCreateAlert) -> models.Alerts:
    # Create a new alert instance and save it to the database
    db_alert = models.Alerts(
        user_id = user_id,
        coin_name = alert.coin_name,
        coin_price_threshold = alert.coin_price_threshold
    )
    
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    
    return db_alert

# Retrieve an alert by its ID
def get_alert_by_id(db: Session, alert_id: int) -> models.Alerts | None:
    return db.query(models.Alerts).filter(models.Alerts.alert_id == alert_id).first()

# Retrieve all active alerts
def get_all_active_alerts(db: Session) -> list[models.Alerts]:
    return db.query(models.Alerts).filter(models.Alerts.is_active == True).all()

# delete an alert by its ID
def delete_alert(db: Session, alert_id: int) -> models.Alerts:
    del_alert = db.query(models.Alerts).filter(models.Alerts.alert_id == alert_id).first()
    
    if del_alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    db.delete(del_alert)
    db.commit()
    
    return del_alert