import os


class Config:
    # Flask-SQLAlchemy reads this URI to create the underlying SQLAlchemy engine.
    # Examples:
    #   - sqlite:///students.db
    #   - postgresql+psycopg://user:pass@localhost:5432/students
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///students.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_VERSION = os.getenv("API_VERSION", "v1")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
