from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base

class Recipient(Base):
    __tablename__ = "recipients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    telegram_chat_id = Column(String, unique=True, index=True, nullable=False)
    recipient_type = Column(String, nullable=False) # 'group', 'individual', 'admin'
    active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
