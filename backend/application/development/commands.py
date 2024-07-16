import click
from flask.cli import with_appcontext
from application.utils.encryption import encrypt_string
from application.models import User


@click.command("add_random_user")
@with_appcontext
def create_random_user():
    """
    Creates a random db entry for the user model
    """

    import application.models.users as user_service
    import random
    import string

    username = ''.join(random.choices(string.ascii_lowercase, k=10))
    password = ''.join(random.choices(string.ascii_lowercase, k=10))

    user_service.register_user(username, password)


    click.echo(f"Created user with username {username} and password {password}")


@click.command("check_user_password")
@click.argument("username")
@click.argument("password")
@with_appcontext
def check_user_password(username, password):
    """
    Checks if a user's password is correct
    :param username: The username to check
    :param password: The password to check
    """

    from application.models import users
    from application.extensions import db
    from application.utils.encryption import check_hashed_value

    user = User.query.filter_by(username=username).first()

    if user is None:
        click.echo("User not found")
        return

    if check_hashed_value(password, user.password_hash):
        click.echo("Password is correct")
    else:
        click.echo("Password is incorrect")


@click.command("change_user_role")
@click.argument("userid")
@click.argument("role")
@with_appcontext
def change_user_role(userid, role):
    """
    Changes a user's role
    :param userid: The user's ID
    :param role: The new role
    """

    from application.models import users as user_service
    user = user_service.change_user_role(userid, role)
    if user is None:
        click.echo("User not found")
    else:
        click.echo(f"Changed user {user.username}'s role to {user.role}")


@click.command("delete_user")
@click.argument("userid")
@with_appcontext
def delete_user(userid):
    """
    Deletes a user
    :param userid: The user's ID
    """

    from application.models import users as user_service
    if user_service.delete_user(userid):
        click.echo("User deleted")
    else:
        click.echo("User not found")