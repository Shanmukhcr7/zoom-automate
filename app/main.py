from contextlib import asynccontextmanager
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
from zoneinfo import ZoneInfo
from app.config import get_settings
from app.scheduler.jobs import process_daily_reminders
from app.api import batches, reminders, dashboard

settings = get_settings()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler(timezone=ZoneInfo(settings.timezone))

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up Course Reminder System...")
    
    scheduler.add_job(
        process_daily_reminders,
        CronTrigger(hour=settings.reminder_hour, minute=settings.reminder_minute, timezone=settings.timezone),
        id="daily_reminder_job",
        replace_existing=True
    )
    scheduler.start()
    logger.info(f"Scheduler started. Next run at {settings.reminder_hour}:{settings.reminder_minute:02d} {settings.timezone}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down...")
    scheduler.shutdown()

app = FastAPI(title="Course Reminder API", lifespan=lifespan)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "timezone": settings.timezone,
        "scheduler": "running" if scheduler.running else "stopped"
    }

app.include_router(batches.router)
app.include_router(reminders.router)
app.include_router(dashboard.router)
