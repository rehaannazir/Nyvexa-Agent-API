from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):

    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.5-flash"
    TEMPERATURE: float = 0
    SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_setting():
    return Setting()
