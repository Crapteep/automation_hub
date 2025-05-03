from src.core.domain.models.user import UserLogin
from src.core.domain.models.auth import Token
from src.core.application.commands.common_commands import CommandRequest, CommandResponse


class LoginUserCommandRequest(UserLogin, CommandRequest):
    """Request model for login user, extending domain UserLogin."""
    pass

class LoginUserCommandResponse(Token, CommandResponse):
    """Response model for user login command."""
    
    @classmethod
    def success(cls, access_token: str):
        return cls(status="success", access_token=access_token, token_type="bearer")