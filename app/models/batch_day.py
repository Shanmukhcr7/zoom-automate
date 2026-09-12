from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class BatchDay(Base):
    __tablename__ = "batch_days"
    
    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("batches.id"), nullable=False)
    day_of_week = Column(String, nullable=False) # MONDAY, TUESDAY, etc.
    
    batch = relationship("Batch", back_populates="days")
    
    __table_args__ = (
        UniqueConstraint('batch_id', 'day_of_week', name='uq_batch_day'),
    )
