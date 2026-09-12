import logging
from datetime import datetime
from zoneinfo import ZoneInfo
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.config import get_settings
from app.models import Batch, BatchDay, CurriculumSession, ScheduledSession, ReminderLog, Recipient
from app.services.zoom_service import ZoomService
from app.services.telegram_service import TelegramService
from app.services.message_service import MessageService

settings = get_settings()
logger = logging.getLogger(__name__)

async def process_daily_reminders():
    """
    Core business logic that runs every day at 11 AM IST.
    """
    logger.info("Starting process_daily_reminders job")
    tz = ZoneInfo(settings.timezone)
    current_datetime = datetime.now(tz)
    today = current_datetime.date()
    today_day = current_datetime.strftime("%A").upper() # MONDAY, TUESDAY, etc.
    
    db: Session = SessionLocal()
    zoom_service = ZoomService()
    telegram_service = TelegramService()
    
    try:
        active_batches = db.query(Batch).filter(Batch.active == True).all()
        
        for batch in active_batches:
            # Check if today is a class day for this batch
            batch_days = [bd.day_of_week for bd in batch.days]
            if today_day not in batch_days:
                logger.info(f"Skipping {batch.name} - Today ({today_day}) is not a class day.")
                continue
                
            week = batch.current_week
            
            # Find Curriculum
            curriculum = db.query(CurriculumSession).filter(
                CurriculumSession.course_id == batch.course_id,
                CurriculumSession.week_number == week,
                CurriculumSession.day_of_week == today_day
            ).first()
            
            if curriculum is None:
                logger.warning(f"⚠️ CURRICULUM NOT FOUND for {batch.name} Week #{week} Day: {today_day}")
                # TODO: Send Admin Alert
                continue
                
            # Get or Create Scheduled Session
            scheduled_session = db.query(ScheduledSession).filter(
                ScheduledSession.batch_id == batch.id,
                ScheduledSession.session_date == today
            ).first()
            
            if not scheduled_session:
                scheduled_session = ScheduledSession(
                    batch_id=batch.id,
                    curriculum_session_id=curriculum.id,
                    session_date=today,
                    week_number=week,
                    day_of_week=today_day
                )
                db.add(scheduled_session)
                db.commit()
                db.refresh(scheduled_session)
                
            # Check if Zoom meeting exists, if not create it
            if not scheduled_session.zoom_meeting_id:
                topic = MessageService.generate_zoom_topic(batch, curriculum)
                start_dt = datetime.combine(today, curriculum.default_start_time).replace(tzinfo=tz)
                
                zoom_info = await zoom_service.create_meeting(
                    topic=topic,
                    start_time=start_dt,
                    duration_minutes=curriculum.default_duration_minutes
                )
                
                if zoom_info:
                    scheduled_session.zoom_meeting_id = zoom_info["id"]
                    scheduled_session.zoom_join_url = zoom_info["join_url"]
                    scheduled_session.zoom_start_url = zoom_info["start_url"]
                    db.commit()
                else:
                    logger.error(f"Failed to create zoom meeting for {batch.name} on {today}")
                    continue
            
            # Prevent Duplicate Reminders
            # Find all relevant recipients (group + individual)
            # For this version, let's just grab the batch's telegram_group_chat_id directly, 
            # or iterate over the Recipients table if configured.
            # Assuming we use the Batch's configured chat ID directly as the primary target:
            
            chat_id = batch.telegram_group_chat_id
            if not chat_id:
                logger.warning(f"No Telegram Group Chat ID configured for {batch.name}")
                continue
                
            # Check idempotency directly on ScheduledSession ID and recipient (if using Recipient table)
            # Since we just have a chat_id on Batch for simplicity, we mock a Recipient check
            # For robust implementation, we should have the recipient in the Recipients table.
            recipient = db.query(Recipient).filter(Recipient.telegram_chat_id == str(chat_id)).first()
            if not recipient:
                # Create it if it doesn't exist
                recipient = Recipient(name=f"{batch.name} Group", telegram_chat_id=str(chat_id), recipient_type="group")
                db.add(recipient)
                db.commit()
                db.refresh(recipient)
            
            already_sent = db.query(ReminderLog).filter(
                ReminderLog.scheduled_session_id == scheduled_session.id,
                ReminderLog.recipient_id == recipient.id,
                ReminderLog.status == "SENT"
            ).first()
            
            if already_sent:
                logger.info(f"Reminder already sent for {batch.name} on {today}. Skipping.")
                continue
                
            # Generate Message
            message = MessageService.generate_reminder_message(batch, curriculum, scheduled_session)
            
            # Send Message
            success = await telegram_service.send_message(chat_id=chat_id, text=message)
            
            # Log Result
            log = ReminderLog(
                scheduled_session_id=scheduled_session.id,
                recipient_id=recipient.id,
                status="SENT" if success else "FAILED",
                error_message=None if success else "Telegram delivery failed"
            )
            db.add(log)
            
            if success:
                scheduled_session.reminder_status = "SENT"
            
            db.commit()

    except Exception as e:
        logger.error(f"Error in process_daily_reminders: {e}")
    finally:
        db.close()
        logger.info("Finished process_daily_reminders job")
