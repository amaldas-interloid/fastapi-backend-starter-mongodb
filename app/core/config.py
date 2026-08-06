from functools import cached_property

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application
    APP_NAME: str
    APP_VERSION: str

    # Server
    HOST: str
    PORT: int

    # Environment
    DEBUG: bool
    LOG_LEVEL: str

    MONGODB_URL: str
    DATABASE_NAME: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()