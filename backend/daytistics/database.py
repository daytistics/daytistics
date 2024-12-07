from sqlmodel import create_engine, SQLModel
import os

engine = None


def setup_db():
    global engine
    engine = create_engine(os.getenv("DATABASE_URL", "sqlite:///db.sqlite"))
