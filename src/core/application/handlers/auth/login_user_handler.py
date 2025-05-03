from src.core.application.services.auth_service import AuthService
from src.core.application.commands.auth.login_user_command import LoginUserCommandResponse, LoginUserCommandRequest
from src.core.application.handlers.common_handlers import CommandHandler
from src.utils.exceptions import CommandExecutionError
from src.core.domain.exceptions.auth import InvalidCredentialsError
from src.core.domain.exceptions.user import InactiveUserError


class LoginUserHandler(CommandHandler[LoginUserCommandRequest, LoginUserCommandResponse]):
    """Handler for login user with access token based on LoginUserCommandRequest."""

    def __init__(self, auth_service: AuthService):
        """Initialize the handler with a AuthService dependency.
        
        Args:
            auth_service: Service responsible for auth-related business logic.
        """
        self._auth_service = auth_service
    

    async def handle(self, command: LoginUserCommandRequest) -> LoginUserCommandResponse:
        """Handle the login a user.
        
        Args:
            command: The command containing user login data (email, password).
        
        Returns:
            LoginUserCommandResponse with the status of the operation and access token.
        
        Raises:
            CommandExecutionError: If authentication fails (e.g. invalid credentials)
        """

        try:
            user = await self._auth_service.authenticate(command) #TODO: Sprawdzić pprzesyłanie tokenu w success
            access_token = await self._auth_service.create_access_token(user.id)
            return LoginUserCommandResponse.success(access_token=access_token)
        except InvalidCredentialsError as e:
            raise CommandExecutionError("Invalid credentials", cause=e) from e
        except InactiveUserError as e:
            raise CommandExecutionError("Inactive user", cause=e) from e
        except Exception as e:
            raise CommandExecutionError("Unexpected error during authenticate user", cause=e) from e
    
    async def __call__(self, command: LoginUserCommandRequest) -> LoginUserCommandResponse:
        return await self.handle(command)