# settings.py
# Configuration and environment variables

import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Modal configuration
    MODAL_APP_NAME: str = "first-aid-coach"

    # API Keys
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    LANGFUSE_PUBLIC_KEY: str = ""
    LANGFUSE_SECRET_KEY: str = ""

    # Database (Supabase)
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""

    # PersonaPlex configuration
    PERSONAPLEX_ENDPOINT: str = ""
    PERSONAPLEX_API_KEY: str = ""

    # WebSocket configuration
    WS_HEARTBEAT_INTERVAL: int = 30  # seconds
    WS_MAX_MESSAGE_SIZE: int = 10_000_000  # 10MB for video frames

    # VLM configuration
    VLM_MODEL: str = "gpt-4o"
    VLM_MAX_TOKENS: int = 500
    FRAME_SAMPLE_INTERVAL: float = 2.5  # seconds

    # Coordinator Agent
    COORDINATOR_MODEL: str = "claude-sonnet-4-20250514"
    COORDINATOR_MAX_TOKENS: int = 1024

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
