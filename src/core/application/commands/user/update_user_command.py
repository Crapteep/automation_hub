from src.core.domain.models.user import UpdateCurrentUser, UpdateUserByAdmin
from src.core.application.commands.common_commands import CommandRequest, CommandResponse


class UpdateCurrentUserCommandRequest(UpdateCurrentUser, CommandRequest):
    """Request model for updating user, extending domain UpdateCurrentUser."""
    pass

class UpdateCurrentUserCommandResponse(CommandResponse):
    """Response model for user update command."""
    pass


class UpdateUserByAdminCommandRequest(UpdateUserByAdmin, CommandRequest):
    ...

class UpdateUserByAdminCommandResponse(CommandResponse):
    ...


UpdateUserCommandRequest = UpdateCurrentUserCommandRequest | UpdateUserByAdminCommandRequest
UpdateUserCommandResponse = UpdateUserByAdminCommandResponse | UpdateCurrentUserCommandResponse