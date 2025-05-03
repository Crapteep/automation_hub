from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str = Field(default="bearer")

class TokenPayload(BaseModel):
    sub: UUID
    exp: Optional[int] = None