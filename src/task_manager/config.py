from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    storage_path: Path = Path.home() / ".task_manager" / "tasks.json"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_prefix="TASKMGR_",
        env_file=".env"
          )


settings = Settings()