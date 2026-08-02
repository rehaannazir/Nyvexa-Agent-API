from pathlib import Path
from sqlmodel import SQLModel, create_engine, Session
from app.core.config import get_setting
from app.core.logging import logger

DB_PATH = Path(__file__).resolve().parent.parent / "memory" / "app.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(f"sqlite:///{DB_PATH}")


def create_table():

    SQLModel.metadata.create_all(engine)
    logger.info("Database tables created (or already exist).")


def get_session():

    with Session(engine) as session:
        yield session
