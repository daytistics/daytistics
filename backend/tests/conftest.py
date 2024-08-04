import pytest
from core import create_app
from dotenv import load_dotenv
from core.extensions import db as _db
from backend.core.services.verificator import Verificator, generate_verification_code
from config import TestConfig
from core.models import User
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import create_refresh_token


@pytest.fixture(scope="session")
def app():
    app = create_app(TestConfig())
    with app.app_context():
        yield app


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()


@pytest.fixture(scope="function")
def db(app):
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.session.rollback()
        _db.drop_all()


@pytest.fixture(scope="function")
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
def protection(app, client, db, verificator, setup_db, reset_db):
    with app.app_context():
        if app.config["TESTING"]:
            pass
        else:
            raise ValueError("Testing is not set to True. Aborting tests.")
    yield


@pytest.fixture(autouse=True)
def reset_db(db):
    db.session.remove()
    db.drop_all()
    db.create_all()
    yield
    db.session.remove()
    db.drop_all()


@pytest.fixture
def refresh_token():
    user = User(
        username="testuser", email="test@example.com", password_hash="TestPassword1!"
    )
    _db.session.add(user)
    _db.session.commit()
    return create_refresh_token(identity="testuser")
