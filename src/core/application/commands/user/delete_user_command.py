from src.core.application.commands.common_commands import CommandRequest, CommandResponse
from uuid import UUID
from typing import Optional

class DeleteUserCommandRequest(CommandRequest):
    """Request model for deleting user."""
    user_id: UUID
    reason: Optional[str] = None

class DeleteUserCommandResponse(CommandResponse):
    """Response model for user deletion command."""
    pass