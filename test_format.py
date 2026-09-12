import asyncio
from datetime import time
from app.services.telegram_service import TelegramService
from app.services.message_service import MessageService
from app.models import Batch, CurriculumSession, ScheduledSession

async def test_message_format():
    batch = Batch(name="Batch #2", current_week=0)
    curriculum = CurriculumSession(
        week_number=0,
        day_of_week="SATURDAY",
        category="Basics of AI Filmmaking",
        topic="Basics of AI Filmmaking, AI Filmmaking Workflow, Upcoming AI Tools & Platforms, How AI is changing Film Making & Content Creation",
        default_start_time=time(19, 0)
    )
    scheduled = ScheduledSession(zoom_join_url="https://zoom.us/j/99769589120?pwd=wVPaYVeSFMLKY2854k0UIf61xpEVPr.1")
    
    message = MessageService.generate_reminder_message(batch, curriculum, scheduled)
    
    service = TelegramService()
    chat_id = "-1002152762911"
    
    print("Sending formatted test message...")
    success = await service.send_message(chat_id, message, retries=0)
    if success:
        print("Success!")
    else:
        print("Failed to send.")

if __name__ == "__main__":
    asyncio.run(test_message_format())
