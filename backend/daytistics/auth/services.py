from typing import Optional

import jwt
from sqlmodel import Session, select
from fastapi import Depends

from daytistics.config import JWT_AUTH_ALGORITHM, SECRET_KEY
from daytistics.exceptions import ConfigurationError
from daytistics.dependencies import get_session
from .models import User


class AuthentificationService:
    @staticmethod
    def get_user_by_access_token(
        access_token: str, session: Session = Depends(get_session)
    ) -> Optional[User]:
        if SECRET_KEY is None:
            raise ConfigurationError(
                "SECRET_KEY environment variable is required for JWT authentication"
            )

        try:
            payload = jwt.decode(
                access_token, SECRET_KEY, algorithms=[JWT_AUTH_ALGORITHM]
            )
            user_id = payload.get("sub")
            token_type = payload.get("type")

            if token_type != "access":
                return None

            statement = select(User).where(User.id == int(user_id))
            user = session.exec(statement).first()
            return user
        except jwt.PyJWTError:
            return None
