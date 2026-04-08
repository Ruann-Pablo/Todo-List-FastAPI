from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "ToDo App API"
    PROJECT_VERSION: str = "1.0.0"
    DATABASE_URL: str = ""
    ACESS_TOKEN_EXPIRE_MINUTES: int = int()
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()
