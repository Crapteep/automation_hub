from dependency_injector import containers, providers

from src.core.application.services.auth_service import AuthService
from src.core.application.handlers.auth.login_user_handler import LoginUserHandler


class AuthContainer(containers.DeclarativeContainer):
    settings = providers.Dependency()
    user_repository = providers.Dependency()

    # Services
    auth_service = providers.Factory(
        AuthService,
        user_repository=user_repository,
    )

    # Handlers
    login_user_handler = providers.Factory(
        LoginUserHandler,
        auth_service=auth_service,
    )
