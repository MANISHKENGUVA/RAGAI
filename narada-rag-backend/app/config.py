from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = Field(default="Narada API", min_length=1, max_length=100)

    @field_validator("app_name")
    @classmethod
    def normalize_app_name(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("App name must not be blank.")
        return normalized


@lru_cache
def get_settings() -> Settings:
    return Settings()
