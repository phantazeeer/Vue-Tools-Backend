from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    ACCESS_TOKEN_LT: int  # minutes
    REFRESH_TOKEN_LT: int  # minutes
    JWT_SECRET_KEY: str
    ENCRYPT_ALG: str

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def ASYNC_DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
