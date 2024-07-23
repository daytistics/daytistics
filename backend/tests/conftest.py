import pytest
from src import create_app
from dotenv import load_dotenv
from src.extensions import db as _db
from src.services.verify import Verificator, generate_verification_code
from config import TestConfig
from src.models import User
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import create_refresh_token


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
    verificator.reset_password_requests.clear()
    verificator.change_password_requests.clear()
    verificator.registration_requests.clear()
    verificator.delete_account_requests.clear()
    yield verificator
    verificator.stop_scheduler()
    del verificator

@pytest.fixture(autouse=True)
def setup_db(db):
    # Clear any existing users or setup your database appropriately
    db.session.query(User).delete()
    db.session.commit()

@pytest.fixture(autouse=True)
def reset_db(db):
    db.session.remove()
    db.drop_all()
    db.create_all()
    yield
    db.session.remove()
    db.drop_all()

@pytest.fixture(scope='function')
def test_user(db):
    user = User(username='test_user', email='test@example.com', password_hash='TestPassword1!')
    db.session.add(user)
    db.session.commit()
    yield user
    db.session.delete(user)
    db.session.commit()
    db.drop_all()

@pytest.fixture
def refresh_token():
    user = User(username='testuser', email='test@example.com', password_hash='TestPassword1!')
    _db.session.add(user)
    _db.session.commit()
    return create_refresh_token(identity='testuser')