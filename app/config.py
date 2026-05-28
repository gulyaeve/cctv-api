# from typing import Literal

from ipaddress import ip_network
from typing import Optional

from faststream.rabbit import RabbitBroker
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import quote, urljoin




class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    TZ: str = "Europe/Moscow"
    # MODE: Literal["DEV", "TEST", "PROD"]
    DOMAIN: str
    LOG_LEVEL: str
    ORIGINS: list
    ALLOWED_SUBNETS: list = ["127.0.0.1/32"]

    @property
    def allowed_subnets(self):
        return [ip_network(subnet) for subnet in self.ALLOWED_SUBNETS]

    ROOT_PATH: str = "/cctv"
    SECURED_PATHS: list = ["admin", "docs", "openapi.json"]

    @property
    def secured_paths(self):
        return [urljoin(f"{self.ROOT_PATH}/", path) for path in self.SECURED_PATHS] + [urljoin("/", path) for path in self.SECURED_PATHS]

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
    RABBITMQ_HOST: Optional[str] = None
    RABBITMQ_PORT: Optional[int] = None
    RABBITMQ_DEFAULT_USER: Optional[str] = None
    RABBITMQ_DEFAULT_PASS: Optional[str] = None

    @property
    def rabbitmq_url(self) -> str | None:
        if self.RABBITMQ_HOST:
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

    KEYCLOAK_BASE_URL: Optional[str] = None
    KEYCLOAK_REALM: Optional[str] = None
    KEYCLOAK_CLIENT_ID: Optional[str] = None
    KEYCLOAK_CLIENT_SECRET: Optional[str] = None

    @property
    def token_url(self) -> str:
        return f"{self.KEYCLOAK_BASE_URL}/realms/{self.KEYCLOAK_REALM}/protocol/openid-connect/token"

    @property
    def auth_url(self) -> str:
        return (
            f"{self.KEYCLOAK_BASE_URL}/realms/{self.KEYCLOAK_REALM}/protocol/openid-connect/auth"
        )

    @property
    def logout_url(self) -> str:
        return f"{self.KEYCLOAK_BASE_URL}/realms/{self.KEYCLOAK_REALM}/protocol/openid-connect/logout"

    @property
    def userinfo_url(self) -> str:
        return f"{self.KEYCLOAK_BASE_URL}/realms/{self.KEYCLOAK_REALM}/protocol/openid-connect/userinfo"

    @property
    def redirect_uri(self) -> str:
        return f"{self.DOMAIN}{self.ROOT_PATH}/api/users/login/callback"


settings = Settings()

broker = RabbitBroker(url=settings.rabbitmq_url)
