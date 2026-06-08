from .database import Base
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

# Database Models

# User Model
class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False, unique=True)
    user_password = Column(String, nullable=False)
    
