from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import EmailStr
from datetime import datetime, timezone


class User(SQLModel, table=True):

    id: Optional[int] = Field(primary_key=True, default=None)
    username: str
    email: EmailStr
    passward_hash: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
