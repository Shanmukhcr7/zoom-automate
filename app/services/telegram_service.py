import httpx
import logging
import asyncio
from typing import Optional, Dict, Any
from app.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

class TelegramService:
    def __init__(self):
        self.token = settings.telegram_bot_token
        self.base_url = f"https://api.telegram.org/bot{self.token}"

    async def get_me(self) -> Dict[str, Any]:
        """Test the bot token."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/getMe")
            return response.json()

    async def send_message(self, chat_id: str, text: str, retries: int = 3) -> bool:
        """Send a message to a specific chat_id with retry logic."""
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }
        
        # Retry logic: 30s, 2m, 5m
        retry_delays = [30, 120, 300]

        async with httpx.AsyncClient(timeout=10.0) as client:
            for attempt in range(retries + 1):
                try:
                    response = await client.post(url, json=payload)
                    response.raise_for_status()
                    data = response.json()
                    
                    if data.get("ok"):
                        logger.info(f"Telegram message sent to {chat_id}")
                        return True
                    else:
                        logger.error(f"Telegram API returned error: {data}")
                        
                except httpx.RequestError as exc:
                    logger.error(f"Request error while requesting {exc.request.url!r}: {exc}")
                except httpx.HTTPStatusError as exc:
                    logger.error(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}")

                if attempt < retries:
                    delay = retry_delays[attempt]
                    logger.warning(f"Telegram send failed. Retrying in {delay} seconds (Attempt {attempt + 1}/{retries})")
                    await asyncio.sleep(delay)
                    
        logger.error(f"Failed to send Telegram message to {chat_id} after {retries} retries.")
        return False

    async def send_admin_alert(self, text: str):
        """Send a message to the admin API key or specific admin chat."""
        # For now, we will use a dedicated admin logic or rely on the recipient table
        pass
