from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext

from daytistics.shared.services import CryptoService, MailService
from daytistics.domains.users.exceptions import (
    UserNotFoundError,
    VerificationFailedError,
    WrongPasswordError,
    InvalidEmailError,
    InvalidPasswordError,
    InvalidUsernameError,
)
from daytistics.domains.users.models import User
from daytistics.domains.users.repositories import UserRepository
from daytistics.domains.users.schemas import UserRegistrationInput
from daytistics.settings import JwtSettings
from daytistics.shared.utils.validation import (
    is_valid_email,
    is_valid_password,
    is_valid_username,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(
        self,
        crypto_service: CryptoService,
        user_repository: UserRepository,
        mail_service: MailService,
    ) -> None:
        self.crypto_service = crypto_service
        self.user_repository = user_repository
        self.mail_service = mail_service

    async def register_user(self, user_input: UserRegistrationInput) -> User:
        user = User(
            username=user_input.username,
            email=user_input.email,
            hashed_password=self.crypto_service.get_hash(user_input.password),
        )

        if not is_valid_email(user.email):
            raise InvalidEmailError

        if not is_valid_username(user_input.username):
            raise InvalidUsernameError

        if not is_valid_password(user_input.password, [user.email, user.username]):
            raise InvalidPasswordError

        created_user = await self.user_repository.create_user(user)
        await self.mail_service.send_registration_verification_email(created_user)

        return created_user

    async def verify_user(self, token: str) -> User:
        data = self.crypto_service.decode_token(token)

        if not data:
            raise VerificationFailedError

        sub = data.get("sub")

        if not sub:
            raise VerificationFailedError

        return await self.user_repository.verify_user(int(sub))

    async def login_user(self, email: str, password: str) -> User:
        user = await self.user_repository.get_user_by_email(email)

        if not user:
            raise UserNotFoundError

        if not pwd_context.verify(password, user.hashed_password):
            raise WrongPasswordError

        return user


class AuthenticationService:
    def __init__(
        self,
        crypto_service: CryptoService,
        user_repository: UserRepository,
        jwt_settings: JwtSettings,
    ) -> None:
        self.crypto_service = crypto_service
        self.user_repository = user_repository
        self.jwt_settings = jwt_settings

    async def generate_refresh_token(self, user: User) -> str:
        exp = datetime.now(timezone.utc) + timedelta(
            minutes=self.jwt_settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )

        if not user.id:
            raise UserNotFoundError

        return self.crypto_service.generate_jwt_token(
            self.crypto_service.TokenType.REFRESH_TOKEN,
            user.id,
            exp,
        )

    async def generate_access_token(self, user: User) -> str:
        exp = datetime.now(timezone.utc) + timedelta(
            minutes=self.jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        if not user.id:
            raise UserNotFoundError

        return self.crypto_service.generate_jwt_token(
            self.crypto_service.TokenType.ACCESS_TOKEN,
            user.id,
            exp,
        )

    async def refresh_access_token(self, token: str) -> str:
        data = self.crypto_service.decode_token(token)

        if not data:
            raise VerificationFailedError

        token_type = data.get("type")

        if token_type != self.crypto_service.TokenType.REFRESH_TOKEN:
            raise VerificationFailedError

        sub = data.get("sub")

        if not sub:
            raise VerificationFailedError

        user = await self.user_repository.get_user_by_id(int(sub))

        if not user:
            raise UserNotFoundError

        return await self.generate_access_token(user)

    async def validate_access_token(self, token: str) -> User | None:
        data = self.crypto_service.decode_token(token)

        if not data:
            return None

        token_type = data.get("type")

        if token_type != self.crypto_service.TokenType.ACCESS_TOKEN:
            return None

        sub = data.get("sub")

        if not sub:
            return None

        user = await self.user_repository.get_user_by_id(int(sub))

        if not user:
            return None

        return user
