from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from pydantic import EmailStr
from datetime import datetime, timezone

class User(SQLModel, table=True):
    id: UUID = Field(default=uuid4, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: EmailStr = Field(unique=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))