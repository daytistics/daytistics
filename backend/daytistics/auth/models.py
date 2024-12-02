from typing import Optional
from datetime import datetime

from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    email: str
    hashed_password: str
    is_active: bool = False
    is_superuser: bool = False
    last_login: Optional[datetime] = None
    date_joined: Optional[datetime] = None
