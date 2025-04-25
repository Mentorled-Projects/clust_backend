import os
from dotenv import load_dotenv
from pydantic import BaseSettings, AnyHttpUrl, validator
from typing import List, Optional

load_dotenv()

class Settings(BaseSettings):
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = ENVIRONMENT == "development"

    PROJECT_NAME: str = "Clust"
    VERSION: str = "1.0.0"

    DATABASE_URL: str = os.getenv("DATABASE_URL")

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    SMTP_SERVER: Optional[str] = os.getenv("SMTP_SERVER")
    SMTP_PORT: Optional[int] = os.getenv("SMTP_PORT")
    EMAILS_FROM_EMAIL: Optional[str] = os.getenv("EMAILS_FROM_EMAIL")

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True

settings = Settings()
