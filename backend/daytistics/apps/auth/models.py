from typing import Optional
from datetime import datetime

from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    email: str
    hashed_password: str
    is_verified: bool = False
    is_locked: bool = False
    is_superuser: bool = False
    last_login: Optional[datetime] = None
    created_at: datetime = Field(default=datetime.now())
    auth_provider: str = Field(default="email", include=["email", "google", "github"])
    provider_user_id: Optional[str] = None
