# app/config.py

import os
from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv()


class Settings(BaseSettings):
    db_url: str


settings = Settings(**{"db_url": os.environ.get("DATABASE_URL")})
