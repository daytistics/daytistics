from sqlmodel import create_engine, SQLModel

engine = None


def setup_db():
    engine = create_engine(
        "postgresql://daytisticsdev:daytisticsdev@database:5432/daytisticsdev"
    )
    SQLModel.metadata.create_all(engine)
