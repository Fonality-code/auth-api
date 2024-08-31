from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", from_attributes=True, extra="ignore"
    )

    APP_NAME: str = "API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = ""
    MONGODB_URL: str | None = None
    DATABASE_NAME: str | None = None

    TESTING: bool = False
    DEBUG: bool = False
