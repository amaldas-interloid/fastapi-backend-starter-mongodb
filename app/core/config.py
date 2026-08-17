from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application
    APP_NAME: str
    APP_VERSION: str

    # Server
    HOST: str
    PORT: int

    # Environment
    DEBUG: bool = False
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    MONGODB_URL: str
    DATABASE_NAME: str

    JWT_SECRET_KEY: str = Field(min_length=32)
    JWT_ALGORITHM: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, gt=0)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, gt=0)

    # seed default password
    SEED_DEFAULT_PASSWORD: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int

    REDIS_RATE_LIMIT: int
    REDIS_RATE_LIMIT_WINDOW: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()  # type: ignore[call-arg]
