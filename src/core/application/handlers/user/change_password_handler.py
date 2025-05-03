from src.core.application.services.user_service import UserService
from src.core.application.commands.user.change_password_comand import ChangePasswordCommandResponse, ChangePasswordCommandRequest
from src.core.application.handlers.common_handlers import CommandHandler
from src.core.domain.exceptions.user import UserAlreadyExistsError, InvalidUserDataError, UserNotFoundError, UserAlreadyInactiveError, InvalidPasswordError, PasswordReuseError
from src.utils.exceptions import CommandExecutionError
from uuid import UUID

class ChangePasswordHandler(CommandHandler[ChangePasswordCommandRequest, ChangePasswordCommandResponse]):
    """Handler for changing password based on ChangePasswordCommandRequest."""

    def __init__(self, user_service: UserService):
        """Initialize the handler with a UserService dependency.
        
        Args:
            user_service: Service responsible for user-related business logic.
        """
        self._user_service = user_service
    

    async def handle(self, user_id: UUID, command: ChangePasswordCommandRequest) -> ChangePasswordCommandResponse:
        """Handle the changing user password.
        
        Args:
            command: The command containing current user id.
        
        Returns:
            ChangePasswordCommandResponse with the status of the operation.
        
        Raises:
            CommandExecutionError:
        """
        try:
            await self._user_service.change_user_password(user_id=user_id, command=command)
            return ChangePasswordCommandResponse.success(message="The password has been successfully changed")
        except UserNotFoundError as e:
            raise CommandExecutionError("User not found", cause=e) from e
        except InvalidPasswordError as e:
            raise CommandExecutionError("Invalid old password.", cause=e) from e
        except PasswordReuseError as e:
            raise CommandExecutionError("New password must be different from the old password.", cause=e) from e
        except Exception as e:
            print(e)
            raise CommandExecutionError("Unexpected error during changing password", cause=e) from e
    
    async def __call__(self, user_id: UUID, command: ChangePasswordCommandRequest) -> ChangePasswordCommandResponse:
        return await self.handle(user_id, command)