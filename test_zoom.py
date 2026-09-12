import asyncio
import httpx
from app.config import get_settings

settings = get_settings()

async def test_zoom_auth():
    print("Testing Zoom Auth...")
    token_url = f"https://zoom.us/oauth/token?grant_type=account_credentials&account_id={settings.zoom_account_id}"
    auth = httpx.BasicAuth(settings.zoom_client_id, settings.zoom_client_secret)
    
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, auth=auth)
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")

if __name__ == "__main__":
    asyncio.run(test_zoom_auth())
