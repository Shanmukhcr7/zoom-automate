from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class ReminderLog(Base):
    __tablename__ = "reminder_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    scheduled_session_id = Column(Integer, ForeignKey("scheduled_sessions.id"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("recipients.id"), nullable=False)
    reminder_type = Column(String, nullable=False, default="daily_reminder")
    status = Column(String, nullable=False) # 'SENT', 'FAILED'
    error_message = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    scheduled_session = relationship("ScheduledSession")
    recipient = relationship("Recipient")

    # Idempotency constraint: Prevent sending the same reminder type to the same recipient for the same session
    __table_args__ = (
        UniqueConstraint('scheduled_session_id', 'recipient_id', 'reminder_type', name='uq_scheduled_session_recipient_type'),
    )
