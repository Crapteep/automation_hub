
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime, timezone

from src.core.domain.models.user import UserResponse



class QueryRequest(BaseModel):
    query_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class QueryResponse(BaseModel):
    query_id: UUID
    success: bool
    error: Optional[str] = None

    @classmethod
    def success_response(cls, query_id: str, user: UserResponse):
        return cls(
            query_id=query_id,
            success=True,
            error=None,
            user=user
        )

class PaginationFilterQuery(BaseModel):
    skip: int = 0
    limit: int = 100
    search: Optional[str] = None
    is_active: Optional[bool] = None
    sort_by: Optional[str] = None
    sort_order: Optional[str] = "asc"