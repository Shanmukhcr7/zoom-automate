from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class BatchDayBase(BaseModel):
    day_of_week: str

class BatchDayResponse(BatchDayBase):
    id: int
    
    class Config:
        from_attributes = True

class BatchBase(BaseModel):
    name: str
    current_week: int
    active: bool = True
    telegram_group_chat_id: Optional[str] = None

class BatchUpdateWeek(BaseModel):
    current_week: int

class BatchResponse(BatchBase):
    id: int
    course_id: int
    days: List[BatchDayResponse] = []
    
    class Config:
        from_attributes = True
