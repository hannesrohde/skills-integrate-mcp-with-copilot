from sqlmodel import SQLModel, create_engine, Session
from typing import Optional
import os


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./activities.db")


def get_engine(url: Optional[str] = None):
    return create_engine(url or DATABASE_URL, echo=False)


def init_db(engine=None):
    eng = engine or get_engine()
    SQLModel.metadata.create_all(eng)
    return eng


def get_session(engine=None):
    eng = engine or get_engine()
    return Session(eng)
