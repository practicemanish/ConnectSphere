"""App settings, loaded once from environment variables and the root .env file."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# config.py -> core -> app -> backend -> project root
ROOT_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    # Real environment variables win over values in .env.
    # extra="ignore" lets .env hold values meant for Docker or the frontend.
    model_config = SettingsConfigDict(env_file=ROOT_DIR / ".env", extra="ignore")

    app_name: str = "ConnectSphere"
    app_env: str = "development"
    database_url: str  # required: startup fails with a clear error if missing


@lru_cache
def get_settings() -> Settings:
    return Settings()
