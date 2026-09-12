import asyncio
from app.services.telegram_service import TelegramService

async def test_telegram():
    service = TelegramService()
    chat_id = "-1002152762911" # Added minus and 100 prefix common for supergroups, will fallback if needed
    message = "🧪 <b>TEST MESSAGE</b>\n\nTelegram automation is working correctly! Course Reminder System is online."
    
    print(f"Attempting to send message to group: {chat_id}")
    success = await service.send_message(chat_id, message, retries=0)
    
    if not success:
        print("Failed with -100 prefix. Trying raw ID...")
        chat_id_raw = "1002152762911"
        success_raw = await service.send_message(chat_id_raw, message, retries=0)
        if success_raw:
            print("Successfully sent with raw ID!")
            return
            
    if success:
        print("Successfully sent with -100 prefix!")

if __name__ == "__main__":
    asyncio.run(test_telegram())
