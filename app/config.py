import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    app_env: str = "development"
    database_url: str
    
    telegram_bot_token: str
    
    zoom_account_id: str
    zoom_client_id: str
    zoom_client_secret: str
    zoom_meeting_passcode: str = "aifm"
    
    admin_api_key: str
    
    timezone: str = "Asia/Kolkata"
    reminder_hour: int = 9
    reminder_minute: int = 0
    default_session_hour: int = 19
    default_session_minute: int = 0
    
    model_config = SettingsConfigDict(env_file=".env")

@lru_cache()
def get_settings():
    return Settings()
