from src.core.application.services.user_service import UserService
from src.core.application.commands.user.deactivate_user_command import DeactivateUserCommandResponse, DeactivateUserCommandRequest
from src.core.application.handlers.common_handlers import CommandHandler
from src.core.domain.exceptions.user import UserAlreadyExistsError, InvalidUserDataError, UserNotFoundError, UserAlreadyInactiveError
from src.utils.exceptions import CommandExecutionError


class DeactivateUserHandler(CommandHandler[DeactivateUserCommandRequest, DeactivateUserCommandResponse]):
    """Handler for deactivate user based on DeactivateUserCommandRequest."""

    def __init__(self, user_service: UserService):
        """Initialize the handler with a UserService dependency.
        
        Args:
            user_service: Service responsible for user-related business logic.
        """
        self._user_service = user_service
    

    async def handle(self, command: DeactivateUserCommandRequest) -> DeactivateUserCommandResponse:
        """Handle the deactivate user.
        
        Args:
            command: The command containing current user id.
        
        Returns:
            DeactivateUserCommandResponse with the status of the operation.
        
        Raises:
            CommandExecutionError:
        """
        try:
            await self._user_service.deactivate_user(command.user_id)
            return DeactivateUserCommandResponse.success(message="The account has been successfully deactivated")
        except UserNotFoundError as e:
            raise CommandExecutionError("User not found", cause=e) from e
        except UserAlreadyInactiveError as e:
            raise CommandExecutionError("User is already inactive.", cause=e) from e
        except Exception as e:
            raise CommandExecutionError("Unexpected error during user creation", cause=e) from e
    
    async def __call__(self, command: DeactivateUserCommandRequest) -> DeactivateUserCommandResponse:
        return await self.handle(command)