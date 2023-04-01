from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    app_name: str = "Truefaces API"
    secret_key: str = os.getenv("SECRET_KEY")
    database_url: str = os.getenv("DATABASE_URL")

settings = Settings()