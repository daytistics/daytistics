from application.development.commands import (
    create_random_user,
    check_user_password,
    change_user_role,
    delete_user
)
from flask import Flask


def load_commands(app: Flask):
    if app.config["USE_DEVELOPMENT_FEATURES"]:
        app.cli.add_command(create_random_user)
        app.cli.add_command(check_user_password)
        app.cli.add_command(change_user_role)
        app.cli.add_command(delete_user)
