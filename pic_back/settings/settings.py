import tomllib
from functools import lru_cache
from pathlib import Path

from pydantic import AliasChoices, Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from pic_back.shared import EnvType, TimeSeconds


class Settings(BaseSettings):
    environment: EnvType = Field(default=EnvType.LOCAL, validation_alias=AliasChoices("environment", "env"))
    database_base_path: Path = Path("./data/database")
    global_api_prefix: str = "/api/v1"

    backup_task_frequency_sec: int = TimeSeconds.DAY.value + TimeSeconds.HOUR.value
    mapper_task_frequency_sec: int = TimeSeconds.HALF_DAY.value

    google_drive_backup_folder_id: str
    google_drive_upload_images_folder_id: str = "13RdM7JHyoDdwr2wdWINeDJQEveTUWtC0"
    google_drive_token_json_file_path: Path = Path("./data/token.json")

    google_client_id: str
    google_api_key: str

    access_token_lifetime_minutes: int = 15
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"

    frontend_base_url: str

    # pagination
    default_page_size: int = 25

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @computed_field
    @property
    def version(self) -> str:
        with open("./pyproject.toml", "rb") as f:
            return tomllib.load(f)["project"]["version"]  # type: ignore


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore [call-arg]
