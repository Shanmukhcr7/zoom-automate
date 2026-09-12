import httpx
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from app.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

class ZoomService:
    def __init__(self):
        self.account_id = settings.zoom_account_id
        self.client_id = settings.zoom_client_id
        self.client_secret = settings.zoom_client_secret
        self.passcode = settings.zoom_meeting_passcode
        self.token_url = f"https://zoom.us/oauth/token?grant_type=account_credentials&account_id={self.account_id}"
        self.api_base_url = "https://api.zoom.us/v2"

    async def _get_access_token(self) -> str:
        """Fetch the Server-to-Server OAuth token."""
        auth = httpx.BasicAuth(self.client_id, self.client_secret)
        async with httpx.AsyncClient() as client:
            response = await client.post(self.token_url, auth=auth)
            response.raise_for_status()
            data = response.json()
            return data["access_token"]

    async def create_meeting(self, topic: str, start_time: datetime, duration_minutes: int = 90) -> Optional[Dict[str, Any]]:
        """Create a Zoom meeting with the specified configurations."""
        try:
            token = await self._get_access_token()
        except Exception as e:
            logger.error(f"Failed to authenticate with Zoom API: {e}")
            return None

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        # Zoom requires UTC time format, or a timezone specified.
        # We will format it properly as YYYY-MM-DDTHH:MM:SS format and provide timezone
        start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")

        payload = {
            "topic": topic,
            "type": 2, # Scheduled meeting
            "start_time": start_time_str,
            "duration": duration_minutes,
            "timezone": settings.timezone,
            "password": self.passcode,
            "settings": {
                "host_video": True,
                "participant_video": False,
                "mute_upon_entry": True,
                "watermark": False,
                "use_pmi": False,
                "approval_type": 2, # No registration required
                "audio": "both",
                "auto_recording": "cloud", # Cloud recording ON
                "waiting_room": False
            }
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(f"{self.api_base_url}/users/me/meetings", headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                logger.info(f"Zoom meeting created: {data.get('id')}")
                return {
                    "id": str(data.get("id")),
                    "join_url": data.get("join_url"),
                    "start_url": data.get("start_url")
                }
            except Exception as e:
                logger.error(f"Failed to create Zoom meeting: {e}")
                return None
