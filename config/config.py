from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", from_attributes=True, extra="ignore"
    )

    APP_NAME: str
    APP_VERSION: str
    APP_DESCRIPTION: str = ""
    MONGODB_URL: str
