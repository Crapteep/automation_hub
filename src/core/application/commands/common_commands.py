from abc import ABC, abstractmethod
from pydantic import BaseModel


class CommandRequest(BaseModel):
    ...


class CommandResponse(BaseModel):
    status: str
    message: str | None = None