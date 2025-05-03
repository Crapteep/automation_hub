from src.core.application.queries.common_queries import QueryResponse, QueryRequest, PaginationFilterQuery
from src.core.domain.models.user import UserResponse, UserId
from typing import Optional


class GetUsersQueryRequest(QueryRequest, PaginationFilterQuery):
    is_superuser: Optional[bool] = None


class GetUsersQueryResponse(QueryResponse):
    users: list[UserResponse]

    @classmethod
    def success_response(cls, query_id: str, users: UserResponse):
        return cls(
            query_id=query_id,
            success=True,
            error=None,
            users=users
        )


