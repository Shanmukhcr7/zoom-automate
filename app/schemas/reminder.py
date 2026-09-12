from pydantic import BaseModel
from datetime import date
from typing import Optional

class ReminderPreviewRequest(BaseModel):
    batch_id: int
    date: date

class ReminderPreviewResponse(BaseModel):
    batch: str
    week: int
    day: str
    category: str
    topic: str
    zoom_topic: str
    zoom_time: str
    message: str

class TestReminderRequest(BaseModel):
    chat_id: Optional[str] = None
