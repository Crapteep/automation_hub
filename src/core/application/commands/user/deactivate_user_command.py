from src.core.domain.models.user import CreateUserData
from src.core.application.commands.common_commands import CommandRequest, CommandResponse
from uuid import UUID

class DeactivateUserCommandRequest(CommandRequest):
    """Request model for creating a new user, extending domain DeactivateUserData."""
    user_id: UUID

class DeactivateUserCommandResponse(CommandResponse):
    """Response model for user creation command."""
    pass