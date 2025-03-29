from src.core.domain.models.user import UserData, UserId
from src.core.application.commands.common_commands import CommandRequest, CommandResponse, Command
from src.core.infrastructure.repositories.user_repository import UserRepository

class CreateUserCommandRequest(UserData, CommandRequest):
    ...

class CreateUserCommandResponse(CommandResponse):
    user_id: UserId


class CreateUserCommand(Command[CreateUserCommandRequest, CreateUserCommandResponse]):
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository


    async def __call__(self, request: CreateUserCommandRequest) -> CreateUserCommandResponse:
        user_data = UserData(
            name=request.username,
            email=request.email
        )

        user_id = await self._user_repository.create(user_data)

        return CreateUserCommandResponse(user_id=user_id)