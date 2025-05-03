from src.core.application.services.user_service import UserService
from src.core.application.commands.user.delete_user_command import DeleteUserCommandResponse, DeleteUserCommandRequest
from src.core.application.handlers.common_handlers import CommandHandler
from src.core.domain.exceptions.user import UserAlreadyExistsError, InvalidUserDataError, UserNotFoundError, UserAlreadyInactiveError, NoPermissionError
from src.utils.exceptions import CommandExecutionError


class DeleteUserHandler(CommandHandler[DeleteUserCommandRequest, DeleteUserCommandResponse]):
    """Handler for Delete user based on DeleteUserCommandRequest."""

    def __init__(self, user_service: UserService):
        """Initialize the handler with a UserService dependency.
        
        Args:
            user_service: Service responsible for user-related business logic.
        """
        self._user_service = user_service
    

    async def handle(self, command: DeleteUserCommandRequest) -> DeleteUserCommandResponse:
        """Handle the Delete user.
        
        Args:
            command: The command containing current user id and optional reason.
        
        Returns:
            DeleteUserCommandResponse with the status of the operation.
        
        Raises:
            CommandExecutionError:
        """
        try:
            await self._user_service.delete_user(command.user_id)
            return DeleteUserCommandResponse.success(message=f"The user {command.user_id} has been successfully deleted.")
        except UserNotFoundError as e:
            raise CommandExecutionError("User not found", cause=e) from e
        except NoPermissionError as e:
            raise CommandExecutionError("No sufficient permissions to remove a user.", cause=e) from e
        except UserAlreadyInactiveError as e:
            raise CommandExecutionError("User is already inactive.", cause=e) from e
        except Exception as e:
            raise CommandExecutionError("Unexpected error during user creation", cause=e) from e
    
    async def __call__(self, command: DeleteUserCommandRequest) -> DeleteUserCommandResponse:
        return await self.handle(command)