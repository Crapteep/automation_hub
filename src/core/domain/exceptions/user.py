

class UserAlreadyExistsError(Exception):
    """Raised when attempting to create a user with an already registered email."""
    
    def __init__(self, message: str = "User with this email already exists"):
        super().__init__(message)
        self.message = message


class InvalidUserDataError(Exception):
    """Raised when user data is invalid (e.g., empty username or weak password)."""
    
    def __init__(self, message: str = "Invalid user data provided"):
        super().__init__(message)
        self.message = message