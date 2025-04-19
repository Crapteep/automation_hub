from abc import ABC, abstractmethod
from pydantic import BaseModel


class QueryRequest(BaseModel):
    ...


class QueryResponse(BaseModel):
    ...


class Query[QueryRequest, QueryResponse](ABC):
    @abstractmethod
    async def __call__(self, request: QueryRequest) -> QueryResponse:
        ...
        