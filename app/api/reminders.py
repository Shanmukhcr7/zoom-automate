from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models import Batch, CurriculumSession, ScheduledSession
from app.schemas.reminder import ReminderPreviewRequest, ReminderPreviewResponse
from app.services.message_service import MessageService
from app.scheduler.jobs import process_daily_reminders

router = APIRouter(prefix="/api/reminders", tags=["Reminders"])

@router.post("/preview", response_model=ReminderPreviewResponse)
def preview_reminder(req: ReminderPreviewRequest, db: Session = Depends(get_db)):
    batch = db.query(Batch).filter(Batch.id == req.batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
        
    day_str = req.date.strftime("%A").upper()
    
    curriculum = db.query(CurriculumSession).filter(
        CurriculumSession.course_id == batch.course_id,
        CurriculumSession.week_number == batch.current_week,
        CurriculumSession.day_of_week == day_str
    ).first()
    
    if not curriculum:
        raise HTTPException(status_code=404, detail=f"No curriculum found for Week {batch.current_week} on {day_str}")

    # Create a dummy scheduled session just for message preview
    dummy_scheduled = ScheduledSession(
        zoom_join_url="https://zoom.us/j/1234567890"
    )
    
    message = MessageService.generate_reminder_message(batch, curriculum, dummy_scheduled)
    topic = MessageService.generate_zoom_topic(batch, curriculum)
    
    return {
        "batch": batch.name,
        "week": batch.current_week,
        "day": day_str,
        "category": curriculum.category,
        "topic": curriculum.topic,
        "zoom_topic": topic,
        "zoom_time": f"{curriculum.default_start_time.strftime('%I:%M %p').lstrip('0')} - 90 mins",
        "message": message
    }

@router.post("/today")
async def trigger_today_reminders(background_tasks: BackgroundTasks):
    """Manually trigger the 11 AM daily job immediately in the background."""
    background_tasks.add_task(process_daily_reminders)
    return {"message": "Daily reminder job triggered in the background."}
