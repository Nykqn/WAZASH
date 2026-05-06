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


settings = Settings()
