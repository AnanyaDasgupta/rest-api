import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///students.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_VERSION = os.getenv("API_VERSION", "v1")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
