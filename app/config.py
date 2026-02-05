from typing import Literal

# во 2 версии Pydantic модуль BaseSettings 
# был вынесен в отдельную библиотеку pydantic-settings
# from pydantic import BaseSettings
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: str

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASS: str
    POSTGRES_DB: str

    @property
    def database_url(self):
        user = f"{self.POSTGRES_USER}:{self.POSTGRES_PASS}"
        database = f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

        return f"postgresql+asyncpg://{user}@{database}"
    
    # TEST_DB_HOST: str
    # TEST_DB_PORT: int
    # TEST_DB_USER: str
    # TEST_DB_PASS: str
    # TEST_DB_NAME: str
    #
    # @property
    # def TEST_DATABASE_URL(self):
    #     return f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"

    # SMTP_HOST: str
    # SMTP_PORT: int
    # SMTP_USER: str
    # SMTP_PASS: str

    REDIS_HOST: str
    REDIS_PORT: int

    # SENTRY_DSN: str

    SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
