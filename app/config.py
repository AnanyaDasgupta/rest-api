import os
from pathlib import Path

from app.db_url import normalize_database_url


class Config:
    # Flask-SQLAlchemy reads this URI to create the underlying SQLAlchemy engine.
    # Examples:
    #   - sqlite:///students.db
    #   - postgresql+psycopg://user:pass@localhost:5432/students
    BASE_DIR = Path(__file__).resolve().parent.parent
    SQLALCHEMY_DATABASE_URI = normalize_database_url(
        os.getenv("DATABASE_URL", "sqlite:///students.db"),
        BASE_DIR,
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_VERSION = os.getenv("API_VERSION", "v1")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
