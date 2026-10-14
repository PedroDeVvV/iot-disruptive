import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine


PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

DEFAULT_DATABASE_URL = (
    "postgresql+psycopg2://iot_user:iot_password@localhost:5432/iot_db"
)


def get_engine():
    database_url = os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)
    return create_engine(database_url)

