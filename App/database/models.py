from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

# Database Models

# User Model - represents users in the system
class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False, unique=True)
    user_password = Column(String, nullable=False)
    
    # Establish relationship with Alerts
    alerts = relationship("Alerts", back_populates="user")

# Alert Model - represents price alerts set by users
class Alerts(Base):
    __tablename__ = "alerts"
    
    alert_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    coin_name = Column(String, nullable=False)
    coin_price_threshold = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    alert_fired_at = Column(DateTime, nullable=True)
    
    # Establish relationship with Users
    user = relationship("Users", back_populates="alerts")