from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Dict, Any
from functools import lru_cache


class Settings(BaseSettings):
    environment: str

    google_client_id: str
    google_api_key: str

    access_token_lifetime_minutes: int
    jwt_secret_key: str
    jwt_algorithm: str

    frontend_base_url: str
    images_page_size: int = 25

    logging: Dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "[{levelname}][{asctime}] {message}",
                "style": "{",
            },
            "simple": {
                "format": "[{levelname}] {message}",
                "style": "{",
            },
        },
        "handlers": {
            "console": {"class": "logging.StreamHandler", "formatter": "simple"},
            "file": {"class": "logging.FileHandler", "filename": "../logs/all.log", "formatter": "verbose"},
        },
        "loggers": {
            "general": {
                "handlers": ["console", "file"],
                "level": "INFO",
            }
        },
    }

    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore [call-arg]
