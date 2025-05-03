from abc import ABC, abstractmethod


class CommandHandler[CommandRequest, CommandResponse](ABC):
    @abstractmethod
    async def handle(self, request: CommandRequest) -> CommandResponse:
        ...
        
