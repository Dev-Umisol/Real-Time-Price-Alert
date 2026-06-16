from pydantic import BaseModel, ConfigDict
from datetime import datetime

# Schemas for user registration and login
class UserRegistration(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    user_name: str
    user_password: str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_name: str
    
class UserLogin(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    user_name: str
    user_password: str