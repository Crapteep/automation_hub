from src.core.application.queries.common_queries import QueryResponse, QueryRequest
from src.core.domain.models.user import UserResponse, UserId
from typing import Optional


class GetUserByIdQueryRequest(QueryRequest):
    user_id: UserId


class GetUserByIdQueryResponse(QueryResponse):
    user: UserResponse


