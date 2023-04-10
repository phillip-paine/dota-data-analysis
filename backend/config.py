from pydantic import BaseSettings


class CommonSettings(BaseSettings):
    APP_NAME: str = "DotA Match Predictions"
    DEBUG_MODE: bool = False


# address of the fastapi host+port
class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000


# mongodb settings: these will be set in environment variables
class DatabaseSettings(BaseSettings):
    DB_URL: str
    DB_NAME: str


class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings()