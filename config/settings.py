from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Threat Detector"
    DEBUG: bool = True

    DATABASE_URL: str = "sqlite:///./app.db"

    ADMIN_USERNAME: str = "taifxa"
    ADMIN_PASSWORD: str = "TzX1726"
    ADMIN_EMAIL: str = "taifxa@gmail.com"

    SECRET_KEY: str = "super-secret-key"
    JWT_ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 1 day

    RATE_LIMIT: int = 10

    class Config:
        env_file = ".env"

settings = Settings()