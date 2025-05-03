from src.utils.exceptions import HttpAwareException


class InvalidCredentialsError(HttpAwareException):
    """Raised when attempting to login user with invalid credentials."""
    status_code = 401
    
    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(message)
        self.message = message
