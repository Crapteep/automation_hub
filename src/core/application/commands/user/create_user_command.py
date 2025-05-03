from src.core.domain.models.user import CreateUserData
from src.core.application.commands.common_commands import CommandRequest, CommandResponse


class CreateUserCommandRequest(CreateUserData, CommandRequest):
    """Request model for creating a new user, extending domain CreateUserData."""
    pass

class CreateUserCommandResponse(CommandResponse):
    """Response model for user creation command."""
    pass