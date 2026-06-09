"""
Application Configuration.

Loads environment variables, defines server settings, database connection strings,
and ML model paths with validation via Pydantic BaseSettings.
"""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Core application settings."""

    APP_NAME: str = "SignSpeak API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # Database configuration
    # Default to local SQLite via aiosqlite for out-of-the-box zero-setup testing,
    # or set DATABASE_URL="postgresql+asyncpg://user:pass@localhost:5432/signspeak" for production
    DATABASE_URL: str = "sqlite+aiosqlite:///./signspeak.db"
    DB_ECHO: bool = False

    # CORS settings
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ]

    # Machine Learning Model Configuration
    MODEL_WEIGHTS_PATH: str = "ml_model/weights/sign_classifier.joblib"
    MIN_CONFIDENCE_THRESHOLD: float = 0.65
    STABILITY_FRAME_COUNT: int = 5

    # Audio & Sentence Builder Settings
    AUTO_TTS_ENABLED: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
