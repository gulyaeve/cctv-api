# from typing import Literal

# во 2 версии Pydantic модуль BaseSettings 
# был вынесен в отдельную библиотеку pydantic-settings
# from pydantic import BaseSettings
from faststream.rabbit import RabbitBroker
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import quote



class Settings(BaseSettings):
    TZ: str = "Europe/Moscow"
    # MODE: Literal["DEV", "TEST", "PROD"]
    DOMAIN: str
    LOG_LEVEL: str
    ORIGINS: list

    ROOT_PATH: str = "/cctv"

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @property
    def database_url(self):
        user = f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
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

    MEDIA_USERNAME: str = Field(default="admin")
    MEDIA_PASSWORD: str = Field(default="admin123")

    REDIS_HOST: str
    REDIS_PORT: int

    # RabbitMQ
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_DEFAULT_USER: str
    RABBITMQ_DEFAULT_PASS: str

    @property
    def rabbitmq_url(self) -> str:
        return (
            f"amqp://{self.RABBITMQ_DEFAULT_USER}:{quote(self.RABBITMQ_DEFAULT_PASS)}@" f"{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}"
        )
    
    QUEUE_NAME: str = "cctv_scr_save"
    QUEUE_NAME_TG: str = "cctv_tg"
    QUEUE_NAME_MAX: str = "cctv_max"
    QUEUE_NAME_AI_TASK: str = "cctv_ai_tasks"

    EXCHANGE_NAME_INPUT: str = "cctv_inc_send"
    EXCHANGE_NAME_OUTPUT: str = "cctv_msg_send"
    EXCHANGE_NAME_AI: str = "cctv_ai"

    # EXCHANGE_NAME: str
    CAMERA_EXCHANGE_NAME: str = "cameras"

    # SENTRY_DSN: str

    SECRET_KEY: str
    ALGORITHM: str
    TOKEN_TTL_MINUTES: int = 30

    TOKEN_BEARER: str = "Admin123"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

broker = RabbitBroker(url=settings.rabbitmq_url)
