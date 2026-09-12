from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Time, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class CurriculumSession(Base):
    __tablename__ = "curriculum_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    week_number = Column(Integer, nullable=False)
    day_of_week = Column(String, nullable=False) # MONDAY, TUESDAY, etc.
    session_order = Column(Integer, nullable=False, default=1)
    
    category = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    description = Column(String, nullable=True)
    
    youtube_url = Column(String, nullable=True)
    drive_url = Column(String, nullable=True)
    docs_url = Column(String, nullable=True)
    canva_url = Column(String, nullable=True)
    other_resource_url = Column(String, nullable=True)
    
    default_start_time = Column(Time, nullable=False)
    default_duration_minutes = Column(Integer, default=90)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    course = relationship("Course")
    
    __table_args__ = (
        UniqueConstraint('course_id', 'week_number', 'day_of_week', 'session_order', name='uq_curriculum_session'),
    )
