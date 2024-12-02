import os
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

import strawberry
from strawberry.types import Info
from strawberry.permission import BasePermission

import jwt
from passlib.context import CryptContext
from pydantic import EmailStr, BaseModel, ValidationError, validator
from sqlmodel import SQLModel, Field, create_engine, Session, select

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration
SECRET_KEY = os.environ.get("SECRET_KEY", secrets.token_hex(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Database setup
DATABASE_URL = "sqlite:///./auth.db"
engine = create_engine(DATABASE_URL)


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = False
    is_superuser: bool = False
    last_login: Optional[datetime] = None
    date_joined: Optional[datetime] = None
    email_verification_token: Optional[str] = None
    email_verification_expires: Optional[datetime] = None

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.hashed_password)

    def generate_jwt_token(
        self, token_type: str = "access", expires_delta: Optional[timedelta] = None
    ) -> str:
        if token_type == "access":
            expires_delta = expires_delta or timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            )
        else:  # refresh token
            expires_delta = expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

        to_encode = {
            "sub": str(self.id),
            "type": token_type,
            "exp": datetime.utcnow() + expires_delta,
        }
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt


def get_user_by_token(token: str) -> Optional[User]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        token_type = payload.get("type")

        if token_type != "access":
            return None

        with Session(engine) as session:
            statement = select(User).where(User.id == int(user_id))
            user = session.exec(statement).first()
            return user
    except jwt.PyJWTError:
        return None


class GraphQLJWTAuth(BasePermission):
    message = "Not authenticated"

    def has_permission(self, source: Any, info: Info) -> bool:
        # Check for authorization header in context
        context = info.context
        authorization = context.get("request").headers.get("Authorization")

        if not authorization or not authorization.startswith("Bearer "):
            return False

        token = authorization.split(" ")[1]
        user = get_user_by_token(token)

        return user is not None


# Pydantic models for validation
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    @validator("username")
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError("Username must be alphanumeric")
        return v


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    user_id: int


@strawberry.type
class AuthResult:
    access_token: str
    refresh_token: str
    user_id: int


@strawberry.mutation
def register(info: Info, input: UserCreate) -> AuthResult:
    with Session(engine) as session:
        # Check if user already exists
        existing_user = session.exec(
            select(User).where(
                (User.username == input.username) | (User.email == input.email)
            )
        ).first()

        if existing_user:
            raise ValueError("Username or email already registered")

        # Create new user
        hashed_password = pwd_context.hash(input.password)
        user = User(
            username=input.username,
            email=input.email,
            hashed_password=hashed_password,
            is_active=False,
            date_joined=datetime.utcnow(),
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        # Generate tokens
        access_token = user.generate_jwt_token("access")
        refresh_token = user.generate_jwt_token("refresh")

        return AuthResult(
            access_token=access_token, refresh_token=refresh_token, user_id=user.id
        )


@strawberry.mutation
def login(info: Info, username: str, password: str) -> AuthResult:
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == username)).first()

        if not user or not user.verify_password(password):
            raise ValueError("Invalid credentials")

        # Update last login
        user.last_login = datetime.utcnow()
        session.add(user)
        session.commit()

        # Generate tokens
        access_token = user.generate_jwt_token("access")
        refresh_token = user.generate_jwt_token("refresh")

        return AuthResult(
            access_token=access_token, refresh_token=refresh_token, user_id=user.id
        )


@strawberry.mutation
def refresh_token(info: Info, refresh_token: str) -> AuthResult:
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        token_type = payload.get("type")

        if token_type != "refresh":
            raise ValueError("Invalid token type")

        with Session(engine) as session:
            user = session.exec(select(User).where(User.id == user_id)).first()

            if not user:
                raise ValueError("User not found")

            # Generate new access and refresh tokens
            new_access_token = user.generate_jwt_token("access")
            new_refresh_token = user.generate_jwt_token("refresh")

            return AuthResult(
                access_token=new_access_token,
                refresh_token=new_refresh_token,
                user_id=user.id,
            )
    except jwt.PyJWTError:
        raise ValueError("Invalid refresh token")


@strawberry.type
class Query:
    @strawberry.field(permission_classes=[GraphQLJWTAuth])
    def me(self, info: Info) -> User:
        # Get the current user from the token
        authorization = info.context["request"].headers.get("Authorization")
        token = authorization.split(" ")[1]
        return get_user_by_token(token)


# Strawberry Schema
schema = strawberry.Schema(query=Query, mutation=register)
