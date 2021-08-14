import logging
import os

from pydantic import BaseSettings


log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    # Paths
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    STATIC_FILES = os.path.abspath(os.path.join(PROJECT_ROOT, "upload"))
    
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "dev")
    DB_URL: str = os.getenv("DB_URL", "sqlite:///arenter.db")

    # PostgreSQL
    POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "postgres")
    POSTGRES_SERVER = os.environ.get("POSTGRES_SERVER", "db")
    POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")
    POSTGRES_DB = os.environ.get("POSTGRES_DB", "arentex")
    DATABASE_URL = os.environ.get(
        "DATABASE_URL",
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )


def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment")
    return Settings()