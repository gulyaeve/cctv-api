from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    TOKEN_BEARER: str
    CAMERAS_API: str

    RTSP_TRANSPORT: str = Field(default="udp")
    MEDIA_SERVER_HOST: str = Field(default="localhost")
    MEDIA_SERVER_PORT: int = Field(default=8554)
    MEDIA_SERVER_PATH: str = Field(default="media")


    @property
    def media_server_rtsp_base_url(self) -> str:
        return f"rtsp://{self.MEDIA_SERVER_HOST}:{self.MEDIA_SERVER_PORT}/{settings.MEDIA_SERVER_PATH}"
    
settings = Settings()