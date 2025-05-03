from src.utils.exceptions import HttpAwareException


class UserAlreadyExistsError(HttpAwareException):
    """Raised when attempting to create a user with an already registered email or username."""
    status_code = 409
    
    def __init__(self, message: str = "User with this email already exists"):
        super().__init__(message)
        self.message = message


class InvalidUserDataError(HttpAwareException):
    """Raised when user data is invalid (e.g., empty username or weak password)."""
    status_code = 422
    
    def __init__(self, message: str = "Invalid user data provided"):
        super().__init__(message)
        self.message = message

    
class UserNotFoundError(HttpAwareException):
    """Raised when user not exists in database"""
    status_code = 404

    def __init__(self, message: str = "User does not exist"):
        super().__init__(message)
        self.message = message


class UsersNotFoundError(HttpAwareException):
    """Raised when users not found in database with given parameters"""
    status_code = 204

    def __init__(self, message: str = "Users not found"):
        super().__init__(message)
        self.message = message



class InactiveUserError(HttpAwareException):
    """Raised when user is inactive."""
    status_code = 401
    
    def __init__(self, message: str = "Inactive user"):
        super().__init__(message)
        self.message = message

class UserAlreadyInactiveError(InactiveUserError):
    status_code = 400


class EmailAlreadyTakenError(HttpAwareException):
    status_code = 409

    def __init__(self, message: str = "Email is already in use"):
        super().__init__(message)
        self.message = message


class UsernameAlreadyTakenError(HttpAwareException):
    status_code = 409

    def __init__(self, message: str = "Username is already in use"):
        super().__init__(message)
        self.message = message

class NoPermissionError(HttpAwareException):
    status_code = 403

    def __init__(self, message: str = "Lack of sufficient permissions"):
        super().__init__(message)
        self.message = message


class InvalidPasswordError(HttpAwareException):
    status_code = 401

    def __init__(self, message: str = "Invalid old password"):
        super().__init__(message)
        self.message = message


class PasswordReuseError(HttpAwareException):
    status_code = 409

    def __init__(self, message: str = "New password must be different from the old password."):
        super().__init__(message)
        self.message = message