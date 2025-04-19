from abc import ABC, abstractmethod

class CommandExecutionError(Exception):
    """Exception raised when a command execution fails."""
    def __init__(self, message: str, cause: Exception | None = None):
        super().__init__(message)
        self.cause = cause
        

class CommandHandler[CommandRequest, CommandResponse](ABC):
    @abstractmethod
    async def handle(self, request: CommandRequest) -> CommandResponse:
        ...
        
