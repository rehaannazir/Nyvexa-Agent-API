from pydantic_settings import BaseSettings


class Setting(BaseSettings):

    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.5-flash"
    TEMPERATURE: float = 0

    class config:
        env_file = ".env"


setting = Setting()
