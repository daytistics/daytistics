import re
from flask_mail import Message, Mail
from flask import current_app


def is_valid_email(email: str) -> bool:
    """
    Checks if an email meets the following criteria:
    - Length is between 3 and 50 characters
    - Contains an @ symbol
    - Contains a valid domain name

    Args:
        email (str): The email address to be validated.

    Returns:
        bool: True if the email is valid, False otherwise.
    """

    if len(email) < 3 or len(email) > 50:
        return False

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        return False

    return True


def send_email(to: str, sender: str, subject: str, body: str) -> bool:
    """
    Sends an email to the specified recipient.

    Args:
        to (str): The email address of the recipient.
        sender (str): The email address of the sender.
        subject (str): The subject of the email.
        body (str): The body content of the email.

    Returns:
        bool: True if the email is sent successfully, False otherwise.
    """

    # ! REMOVE LATER: JUST TO SAVE EMAIL TRAFFIC
    current_app.logger.info(f"Email to: {to}\nSubject: {subject}\nBody: {body}")
    return True

    try:
        with current_app.app_context():
            mail = Mail(current_app)
            msg = Message(subject, sender=sender, recipients=[to])
            msg.body = body
            mail.send(msg)
        return True
    except:
        return False


def send_registration_request_email(to: str, code: str) -> bool:
    """
    Sends a registration request email to the specified recipient.

    Args:
        to (str): The email address of the recipient.
        code (str): The verification code for the registration.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """

    try:
        send_email(
            to=to,
            sender="noreply@daytistics.de",
            subject="Account Erstellung",
            body=f"Hallo {to},\n\nVielen Dank für Deine Registrierung bei Daytistics. Bitte bestätige Deine E-Mail-Adresse, indem Du auf den folgenden Link klickst: http://localhost:5000/verify/{code}\n\nAlternativ kannst du auch den folgenden Code im Browser eingeben: {code} \n\nMit freundlichen Grüßen,\nIhr Daytistics-Team",
        )
        return True
    except:
        return False
