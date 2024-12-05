from datetime import datetime, timedelta, timezone

import pytest
from freezegun import freeze_time
from sqlmodel import Session

from daytistics.modules.auth.services import AuthenticationService
from daytistics.config import SecurityConfig
from tests.factories import ModernUserFactory
from faker import Faker


class TestAuthenticationService:
    @pytest.fixture
    def service(self):
        return AuthenticationService()

    @pytest.mark.parametrize(
        "is_refresh_token",
        [True, False],
    )
    def test_decode_token(
        self,
        service: AuthenticationService,
        security_config: SecurityConfig,
        session: Session,
        is_refresh_token: bool,
    ):
        user = ModernUserFactory.build()
        session.add(user)
        session.commit()
        session.refresh(user)

        with freeze_time(datetime.now(timezone.utc)):
            if is_refresh_token:
                token = service.generate_refresh_token(user, security_config)
            else:
                token = service.generate_access_token(user, security_config)

            decoded = service.decode_token(
                token,
                security_config,
            )

            if is_refresh_token:
                expected_exp = int(
                    (
                        datetime.now(timezone.utc)
                        + timedelta(
                            minutes=security_config.REFRESH_TOKEN_EXPIRE_MINUTES
                        )
                    ).timestamp()
                )
            else:
                expected_exp = int(
                    (
                        datetime.now(timezone.utc)
                        + timedelta(minutes=security_config.ACCESS_TOKEN_EXPIRE_MINUTES)
                    ).timestamp()
                )

            if is_refresh_token:
                assert decoded == {
                    "sub": str(user.id),
                    "type": "refresh",
                    "exp": expected_exp,
                }
            else:
                assert decoded == {
                    "sub": str(user.id),
                    "type": "access",
                    "exp": expected_exp,
                }
