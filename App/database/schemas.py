from pydantic import BaseModel, ConfigDict
from datetime import datetime

# Schemas for user registration and login
class UserRegistration(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    user_name: str
    user_password: str

# Schema for user response after registration or login
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_name: str

# Schema for user login
class UserLogin(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    user_name: str
    user_password: str

# Schema for token response after successful login
class UserToken(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    access_token: str
    token_type: str

# Schema for creating a new alert
class UserCreateAlert(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    coin_name: str
    coin_price_threshold: float

# Schema for creating a new alert
class UserAlertResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    user_id: int
    alert_id: int
    coin_name: str
    coin_price_threshold: float
    alert_fired_at: None | datetime
    is_active: bool