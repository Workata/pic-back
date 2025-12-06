from enum import Enum
from functools import lru_cache
from pathlib import Path

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvType(str, Enum):
    LOCAL = "local"
    DEV = "dev"
    TEST = "test"
    STAGING = "staging"
    ACCEPTANCE = "acceptane"
    PROD = "production"


class Settings(BaseSettings):
    environment: EnvType = Field(default=EnvType.LOCAL, validation_alias=AliasChoices("environment", "env"))
    database_base_path: Path = Path("./data/database")
    global_api_prefix: str = "/api/v1"

    google_drive_backup_folder_id: str

    google_client_id: str
    google_api_key: str

    access_token_lifetime_minutes: int = 15
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"

    frontend_base_url: str

    # pagination
    default_page_size: int = 25

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore [call-arg]
