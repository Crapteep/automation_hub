from abc import ABC, abstractmethod
from pydantic import BaseModel



class CommandRequest(BaseModel):
    ...


class CommandResponse(BaseModel):
    ...


class Command[CommandRequest, CommandResponse](ABC):
    @abstractmethod
    async def __call__(self, request: CommandRequest) -> CommandResponse:
        ...


