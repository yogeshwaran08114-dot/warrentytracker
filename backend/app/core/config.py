from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = "sqlite:///./warrantyhub.db"
    FRONTEND_URL: str = "http://localhost:5173"
    APP_NAME: str = "WarrantyHub"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"


settings = Settings()
