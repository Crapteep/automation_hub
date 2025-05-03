from abc import ABC, abstractmethod
from pydantic import BaseModel


class CommandRequest(BaseModel):
    ...


class CommandResponse(BaseModel):
    status: str
    message: str | None = None

    @classmethod
    def success(cls, message: str = None):
        return cls(status="success", message=message)