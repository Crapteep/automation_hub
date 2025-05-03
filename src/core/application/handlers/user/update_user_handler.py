from src.core.application.services.user_service import UserService
from src.core.application.commands.user.update_user_command import (
    UpdateUserCommandRequest,
    UpdateUserCommandResponse,
    UpdateCurrentUserCommandRequest,
    UpdateCurrentUserCommandResponse,
    UpdateUserByAdminCommandRequest,
    UpdateUserByAdminCommandResponse
)
from src.core.application.handlers.common_handlers import CommandHandler
from src.core.domain.exceptions.user import UserAlreadyExistsError, InvalidUserDataError, UserAlreadyInactiveError, UserNotFoundError
from src.utils.exceptions import CommandExecutionError
from uuid import UUID



class UpdateUserHandler(CommandHandler[UpdateUserCommandRequest, UpdateUserCommandResponse]):
    def __init__(self, user_service: UserService):
        self._user_service = user_service
    

    async def handle(self,
                     user_id: UUID,
                     command: UpdateUserCommandRequest
    ) -> UpdateUserCommandResponse:
        try:
            await self._user_service.update_user(user_id=user_id, data=command)
            if isinstance(command, UpdateUserByAdminCommandRequest):
                return UpdateUserByAdminCommandResponse.success(message="Successfully updated the user")
            return UpdateCurrentUserCommandResponse.success("Successfully updated the user")
        except UserAlreadyInactiveError as e:
            raise CommandExecutionError("User is already inactive.", cause=e) from e
        except UserNotFoundError as e:
            raise CommandExecutionError(message="Users not found", cause=e) from e
        except Exception as e:
            print(e)
            raise CommandExecutionError("Unexpected error during update user", cause=e) from e
    
    async def __call__(self,
                       user_id: UUID,
                       command: UpdateUserCommandRequest) -> UpdateUserCommandResponse:
        return await self.handle(user_id=user_id, command=command)