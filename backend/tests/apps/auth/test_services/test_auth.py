from datetime import datetime, timedelta, timezone

import pytest
from freezegun import freeze_time
from sqlmodel import Session

from daytistics.apps.auth.services.auth import AuthenticationService
from daytistics.config import SecurityConfig


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
        is_refresh_token: bool,
    ):
        USER_ID = 1

        security_config = SecurityConfig()

        with freeze_time(datetime.now(timezone.utc)):
            if is_refresh_token:
                token = service.generate_refresh_token(USER_ID)
            else:
                token = service.generate_access_token(USER_ID)

            decoded = service.decode_token(
                token,
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
                    "sub": str(USER_ID),
                    "type": "refresh",
                    "exp": expected_exp,
                }
            else:
                assert decoded == {
                    "sub": str(USER_ID),
                    "type": "access",
                    "exp": expected_exp,
                }
