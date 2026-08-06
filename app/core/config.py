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
    
    # Database
    DB_HOST: str 
    DB_PORT: int 
    DB_NAME: str 
    DB_USER: str 
    DB_PASSWORD: str 

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    @cached_property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}"
            f"/{self.DB_NAME}"
        )


settings = Settings()