from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class ScheduledSession(Base):
    __tablename__ = "scheduled_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("batches.id"), nullable=False)
    curriculum_session_id = Column(Integer, ForeignKey("curriculum_sessions.id"), nullable=False)
    
    session_date = Column(Date, nullable=False)
    week_number = Column(Integer, nullable=False)
    day_of_week = Column(String, nullable=False)
    
    zoom_meeting_id = Column(String, nullable=True)
    zoom_join_url = Column(String, nullable=True)
    zoom_start_url = Column(String, nullable=True)
    
    reminder_status = Column(String, default="PENDING") # PENDING, SENT, FAILED
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    batch = relationship("Batch")
    curriculum_session = relationship("CurriculumSession")
    
    __table_args__ = (
        UniqueConstraint('batch_id', 'session_date', name='uq_batch_session_date'),
    )
