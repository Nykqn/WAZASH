"""Configuration centralisée de l'application."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Paramètres de l'application."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "WAZASH"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"
    secret_key: str = "dummy-secret-key-for-skeleton-only"
    database_url: str = "sqlite:///./wazash.db"
    jwt_secret_key: str = "dev-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    agent_api_key: str = "wazash-agent-key-2026"
    cors_origins: list[str] = ["http://localhost:8080", "http://127.0.0.1:8080"]


settings = Settings()
