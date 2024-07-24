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

def send_email(to: str, sender: str, subject: str, body: str) -> None:
    with current_app.app_context():
        mail = Mail(current_app)
        msg = Message(subject, sender=sender, recipients=[to])
        msg.body = body
        mail.send(msg)

def send_password_reset_email(to: str, new_password: str) -> None:
    """
    Sends a password reset email
    :param to: The recipient
    """

    send_email(to=to, sender="noreply@daytistics.de", subject="Your new password", body=f"Your new password is: {new_password}")

def send_registration_request_email(to: str, code: str) -> None:
    """
    Sends a verification email
    :param to: The recipient
    :param code: The code
    """
    
    send_email(
        to=to, 
        sender="noreply@daytistics.de", 
        subject="Account Erstellung", 
        body=f"Hallo {to},\n\nVielen Dank für Deine Registrierung bei Daytistics. Bitte bestätige Deine E-Mail-Adresse, indem Du auf den folgenden Link klickst: http://localhost:5000/verify/{code}\n\nAlternativ kannst du auch den folgenden Code im Browser eingeben: {code} \n\nMit freundlichen Grüßen,\nIhr Daytistics-Team"
        )
    
    