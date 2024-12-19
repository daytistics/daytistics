from datetime import datetime, timedelta, timezone

from ..exceptions.email import EmailNotSentError


from typing import List

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr, SecretStr

from daytistics.domains.users.models import User
from daytistics.settings import MailSettings
from daytistics.libs.templates import jinja2

from ._crypto import CryptoService


class MailService:
    def __init__(
        self, crypto_service: CryptoService, mail_settings: MailSettings
    ) -> None:
        self.crypto_service = crypto_service
        self.mail_settings = mail_settings

        conf = ConnectionConfig(
            MAIL_USERNAME="",  # Leer lassen, da MailHog keine Authentifizierung benötigt
            MAIL_PASSWORD=SecretStr(""),  # Leer lassen
            MAIL_FROM="no-reply@daytistics.com",  # Beliebige Absenderadresse
            MAIL_PORT=1025,  # Port von MailHog
            MAIL_SERVER="mailhog",  # MailHog läuft lokal
            MAIL_STARTTLS=False,  # Deaktivieren, da MailHog kein TLS benötigt
            MAIL_SSL_TLS=False,  # Deaktivieren
            USE_CREDENTIALS=False,  # Keine Authentifizierung erforderlich
            VALIDATE_CERTS=False,  # Zertifikatsprüfung deaktivieren
        )

        self.fm = FastMail(conf)

    class _EmailSchema(BaseModel):
        recipients: List[EmailStr]
        html: str

    async def _send_email(self, schema: _EmailSchema):
        message = MessageSchema(
            subject="Daytistics - Account Verification",
            recipients=schema.recipients,
            body=schema.html,
            subtype=MessageType.html,
        )

        await self.fm.send_message(message)

    async def send_registration_verification_email(self, user: User):
        if user.is_verified:
            raise EmailNotSentError("USER_ALREADY_VERIFIED")

        if not user.id:
            raise EmailNotSentError("USER_ID_NOT_SET")

        token = self.crypto_service.generate_jwt_token(
            self.crypto_service.TokenType.ACCOUNT_VERIFICATION,
            user.id,
            datetime.now(timezone.utc) + timedelta(days=24),
        )

        context = {
            "user_email": user.email,
            "verification_url": token,  # TODO: Implementieren
        }
        html = jinja2.get_template("mail/account-verification.html").render(context)

        try:
            await self._send_email(
                self._EmailSchema(recipients=[user.email], html=html)
            )
        except Exception:
            raise EmailNotSentError("EMAIL_SEND_ERROR")

        return token
