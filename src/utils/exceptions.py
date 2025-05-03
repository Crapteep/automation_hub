
class CommandExecutionError(Exception):
    """Exception raised when a command execution fails."""
    def __init__(self, message: str, cause: Exception | None = None):
        super().__init__(message)
        self.cause = cause


class HttpAwareException(Exception):
    status_code: int = 400

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

