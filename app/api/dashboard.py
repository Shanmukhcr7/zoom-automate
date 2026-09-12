from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from zoneinfo import ZoneInfo

from app.database import get_db
from app.models import Batch, CurriculumSession, ScheduledSession
from app.config import get_settings

settings = get_settings()
router = APIRouter(tags=["Dashboard"])
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def get_dashboard(request: Request, db: Session = Depends(get_db)):
    tz = ZoneInfo(settings.timezone)
    current_dt = datetime.now(tz)
    today = current_dt.date()
    today_day_str = current_dt.strftime("%A").upper()

    active_batches = db.query(Batch).filter(Batch.active == True).all()
    
    dashboard_data = []
    
    for batch in active_batches:
        batch_days = [bd.day_of_week for bd in batch.days]
        has_class_today = today_day_str in batch_days
        
        curriculum = None
        scheduled = None
        
        if has_class_today:
            curriculum = db.query(CurriculumSession).filter(
                CurriculumSession.course_id == batch.course_id,
                CurriculumSession.week_number == batch.current_week,
                CurriculumSession.day_of_week == today_day_str
            ).first()
            
            scheduled = db.query(ScheduledSession).filter(
                ScheduledSession.batch_id == batch.id,
                ScheduledSession.session_date == today
            ).first()

        dashboard_data.append({
            "batch": batch,
            "days": ", ".join([bd.day_of_week.capitalize() for bd in batch.days]),
            "has_class_today": has_class_today,
            "curriculum": curriculum,
            "scheduled": scheduled
        })

    return templates.TemplateResponse(
        "dashboard.html", 
        {
            "request": request, 
            "today_str": current_dt.strftime("%A, %d-%m-%Y"),
            "dashboard_data": dashboard_data
        }
    )
