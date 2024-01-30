from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings management class for the application.

    This class is responsible for loading and storing configuration settings
    for the application.

    Args:
        BaseSettings (BaseSettings): Inherits from Pydantic's BaseSettings for
        environment management.
    """

    bot_token: SecretStr
    ai_token: SecretStr

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


config = Settings()
