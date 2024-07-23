import os
from dotenv import load_dotenv, dotenv_values
import ast

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv(".env")
env_vars = dotenv_values(".env")


class Config:
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'

    DATABASE_USER = os.environ.get("DATABASE_USER")
    DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
    DATABASE_HOST = os.environ.get("DATABASE_HOST")
    DATABASE_PORT = os.environ.get("DATABASE_PORT")
    DATABASE_NAME = os.environ.get("DATABASE_NAME")
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URI")
        or f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USE_DEVELOPMENT_FEATURES = os.environ.get("USE_DEVELOPMENT_FEATURES") or False

    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

    MAIL_USE_TLS = True  # bool(ast.literal_eval(os.environ.get('MAIL_USE_TLS')))
    MAIL_USE_SSL = True  # bool(ast.literal_eval(os.environ.get('MAIL_USE_SSL')))

    BACKEND_IP = os.environ.get("BACKEND_IP")
    FRONTEND_IP = os.environ.get("FRONTEND_IP")


class TestConfig(Config):
    load_dotenv("tests/tests.env", override=True)
    env_vars.update(dotenv_values("tests/tests.env"))

    DATABASE_USER = os.environ.get("TEST_DATABASE_USER")
    DATABASE_PASSWORD = os.environ.get("TEST_DATABASE_PASSWORD")
    DATABASE_HOST = os.environ.get("TEST_DATABASE_HOST")
    DATABASE_PORT = os.environ.get("TEST_DATABASE_PORT")
    DATABASE_NAME = os.environ.get("TEST_DATABASE_NAME")
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("TEST_DATABASE_URI")
        or f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
    )

    BACKEND_IP = os.environ.get("BACKEND_IP")
    FRONTEND_IP = os.environ.get("FRONTEND_IP")