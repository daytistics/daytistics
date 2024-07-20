import re
from flask_mail import Message, Mail
from flask import current_app

def is_valid_email(email: str) -> bool:
    """
    Checks if an email is valid
    :param email: The email to check
    :return: True if the email is valid, False otherwise
    """
    if len(email) < 3 or len(email) > 50:
        return False

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False

    return True

def is_email_in_use(email: str) -> bool:
    """
    Checks if an email is in use
    :param email: The email to check
    :return: True if the email is in use, False otherwise
    """
    from src.models import users

    try:
        user = users.User.query.filter_by(email=email).first()
    except:
        return False

    if user is not None:
        return True

    return False

def send_email(to: str, sender: str, subject: str, body: str) -> None:

    with open("../email-test.txt", "w") as f:
        f.write(f"Email sent to {to} from {sender} with subject {subject} and body {body}")

    # with current_app.app_context():
    #     mail = Mail(current_app)
    #     msg = Message(subject, sender=sender, recipients=[to])
    #     msg.body = body
    #     mail.send(msg)

def send_verification_email(to: str, code: str) -> None:
    """
    Sends a verification email
    :param to: The recipient
    :param code: The code
    """
    
    send_email(to=to, sender="noreply@daytistics.de", subject="Daytistics Verification", body=f"Your code is: {code}")
    