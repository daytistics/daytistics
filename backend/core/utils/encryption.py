from flask_bcrypt import Bcrypt
from flask import current_app


def generate_password_hash(password: str, rounds=None, prefix=None) -> str:
    with current_app.app_context():
        bcrypt = Bcrypt(current_app)

        return bcrypt.generate_password_hash(password, rounds, prefix).decode("utf-8")


def check_password_hash(password: str, pw_hash: str) -> bool:
    with current_app.app_context():
        bcrypt = Bcrypt(current_app)

        return bcrypt.check_password_hash(pw_hash, password)
