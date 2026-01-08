from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "DailyTask 2026"
    API_KEY: str = os.getenv("API_KEY", "daily-task-secret-key-2026")

    class Config:
        env_file = ".env"

settings = Settings()
