import pytest

from sqlmodel import create_engine, Session, SQLModel, StaticPool

from daytistics.config import SecurityConfig


@pytest.fixture
def security_config():
    config = SecurityConfig()

    config.SECRET_KEY = "test"
    return config


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
