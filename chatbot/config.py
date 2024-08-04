from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    GENAI_API_KEY: SecretStr
    PERSISTENCE_FILEPATH: str = 'chatbot_persistence'

    class Config:
        env_file = '.env'
        env_encoding = 'utf-8'


settings = Settings()
