# import jwt
# from datetime import datetime, timedelta, timezone
# from daytistics.config import SECRET_KEY, JWT_ALGORITHM
# from daytistics.exceptions import ConfigurationError
# from datetime import datetime, timedelta, timezone
# from typing import Annotated, Any

# import jwt
# from sqlmodel import Session
# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jwt.exceptions import InvalidTokenError
# from passlib.context import CryptContext

# from daytistics.dependencies import get_session
# from .models import User
# from .exceptions import UserNotFoundError

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     if not SECRET_KEY:
#         raise ConfigurationError(
#             "SECRET_KEY environment variable is required for JWT authentication"
#         )

#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.now(timezone.utc) + expires_delta
#     else:
#         expire = datetime.now(timezone.utc) + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)
#     return encoded_jwt


# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)


# def get_password_hash(password):
#     return pwd_context.hash(password)


# async def get_user(email: str) -> Any | None:
#     session = get_session()

#     if not user:
#         raise UserNotFoundError()

#     return user


# def authenticate_user(email: str, password: str):
#     user = get_user()
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user


# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except InvalidTokenError:
#         raise credentials_exception
#     user = get_user(fake_users_db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user


# async def get_current_active_user(
#     current_user: Annotated[User, Depends(get_current_user)],
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user
