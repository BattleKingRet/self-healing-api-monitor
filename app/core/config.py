import os

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "self-healing-api-monitor")
    ENV: str = os.getenv("ENV", "dev")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
