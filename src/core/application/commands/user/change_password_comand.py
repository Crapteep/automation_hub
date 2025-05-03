from src.core.domain.models.user import CreateUserData
from src.core.application.commands.common_commands import CommandRequest, CommandResponse
from uuid import UUID
from pydantic import Field

class ChangePasswordCommandRequest(CommandRequest):
    """Request model for changing user password."""
    old_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8)

class ChangePasswordCommandResponse(CommandResponse):
    """Response model for change password command."""
    pass