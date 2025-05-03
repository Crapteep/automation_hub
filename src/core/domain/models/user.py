from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from pydantic import EmailStr, BaseModel, field_validator
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime

from typing import TypeAlias, Optional
from uuid import UUID


UserId: TypeAlias = UUID

class PasswordValidatorMixin(BaseModel):
    @field_validator("password", check_fields=False)
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must contain at least one digit")
        if not any(c.isupper() for c in value):
            raise ValueError("Password must contain at least one uppercase letter")
        return value



class UserData(BaseModel):
    """Base model for user data."""
    username: str
    email: EmailStr

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        """Validate that username contains only allowed characters and length."""
        if not (3 <= len(value) <= 50):
            raise ValueError("Username must be between 3 and 50 characters")
        if not value.isalnum():
            raise ValueError("Username must contain only alphanumeric characters")
        return value

class User(SQLModel, UserData, table=True):
    """User model in the database."""
    id: UserId = Field(default_factory=uuid4, primary_key=True)
    hashed_password: Optional[str]
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True)), default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True)), default_factory=lambda: datetime.now(timezone.utc))
    username: str = Field(index=True, unique=True)
    email: EmailStr = Field(unique=True)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)

class CreateUserData(UserData, PasswordValidatorMixin):
    """Model for creating a new user."""
    password: str

class CreateUserDBData(UserData):
    hashed_password: str

class UserResponse(BaseModel):
    id: UserId
    username: str
    email: EmailStr
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: str
    password: str


class UpdateCurrentUser(UserData):
    email: Optional[EmailStr] = None
    username: Optional[str] = None


class UpdateUserByAdmin(UpdateCurrentUser):
    is_superuser: Optional[bool] = None
    is_active: Optional[bool] = None

