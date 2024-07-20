import pytest
from src import create_app
from dotenv import load_dotenv
from src.extensions import db as _db
from src.models.users import Verificator
from config import TestConfig
from src.models import User

@pytest.fixture(scope='session')
def app():
    app = create_app(TestConfig())
    with app.app_context():
        yield app

@pytest.fixture(scope='session')
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def db(app):
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.session.rollback()
        _db.drop_all()

@pytest.fixture(scope='function')
def verificator():
    verificator = Verificator()
    yield verificator
    del verificator

@pytest.fixture(autouse=True)
def setup_db(db):
    # Clear any existing users or setup your database appropriately
    db.session.query(User).delete()
    db.session.commit()