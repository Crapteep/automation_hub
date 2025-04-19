
from src.core.infrastructure.repositories.user_repository import UserRepository
from src.core.domain.models.user import User, CreateUserData
from src.core.application.commands.user.create_user_command import CreateUserCommandRequest
from src.core.domain.exceptions.user import InvalidUserDataError, UserAlreadyExistsError

from uuid import UUID

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    

    async def create_user(self, command: CreateUserCommandRequest) -> None:
        """Create a new user based on the provided command.

        Args:
            command: The command containing user creation data (username, email, password).

        Raises:
            UserAlreadyExistsError: If a user with the given email already exists.
            InvalidUserDataError: If the provided data is invalid (e.g., empty username).
        """
        if not command.username.strip():
            raise InvalidUserDataError("Username cannot be empty")
        
        if command.username.lower() in {"admin", "root"}:
            raise InvalidUserDataError("Username is reserved and cannot be used")
        
        existing_user = await self.user_repository.fetch_by_email(command.email)
        if existing_user:
            raise UserAlreadyExistsError(f"User with email {command.email} already exists")

        user_data = CreateUserData(
            username=command.username,
            email=command.email,
            hashed_password=command.password #TODO: Do poprawy hashowanie hasła
        )

        return await self.user_repository.create(user_data)
    

    async def get_user(self, user_id: UUID) -> User | None:
        """Fetch a user by their ID.

        Args:
            user_id: The UUID of the user to fetch.

        Returns:
            The User object if found, else None.
        """
        return await self.user_repository.fetch(user_id)
    
    