from src.core.application.services.user_service import UserService
from src.core.domain.models.user import User
from src.core.application.commands.user.create_user_command import CreateUserCommandResponse, CreateUserCommandRequest
from src.core.application.handlers.common_handlers import CommandHandler, CommandExecutionError
from src.core.domain.exceptions.user import UserAlreadyExistsError, InvalidUserDataError


class CreateUserHandler(CommandHandler[CreateUserCommandRequest, CreateUserCommandResponse]):
    """Handler for creating a new user based on CreateUserCommandRequest."""

    def __init__(self, user_service: UserService):
        """Initialize the handler with a UserService dependency.
        
        Args:
            user_service: Service responsible for user-related business logic.
        """
        self._user_service = user_service
    

    async def handle(self, command: CreateUserCommandRequest) -> CreateUserCommandResponse:
        """Handle the creation of a new user.
        
        Args:
            command: The command containing user creation data (username, email, password).
        
        Returns:
            CreateUserCommandResponse with the status of the operation.
        
        Raises:
            CommandExecutionError: If user creation fails (e.g., duplicate email).
        """
        try:
            await self._user_service.create_user(command)
            return CreateUserCommandResponse(status="success")
        except UserAlreadyExistsError as e:
            raise CommandExecutionError("User already exists", cause=e) from e
        except InvalidUserDataError as e:
            raise CommandExecutionError("Invalid user data", cause=e) from e
    
    async def __call__(self, command: CreateUserCommandRequest) -> CreateUserCommandResponse:
        return await self.handle(command)