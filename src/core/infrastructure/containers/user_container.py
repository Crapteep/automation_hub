from dependency_injector import containers, providers

from src.core.infrastructure.repositories.user_repository import UserRepository
from src.core.application.services.user_service import UserService
from src.core.application.handlers.user.create_user_handler import CreateUserHandler

class UserContainer(containers.DeclarativeContainer):
    settings = providers.Dependency()
    db = providers.Dependency()


    user_repository = providers.Factory(
        UserRepository, 
        db=db
        )

    # Services
    user_service = providers.Factory(
        UserService, 
        user_repository=user_repository
        )
    
    # Commands


    # Queries


    # Handlers
    create_user_handler = providers.Factory(
        CreateUserHandler,
        user_service=user_service
    )

