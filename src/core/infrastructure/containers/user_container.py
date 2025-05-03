from dependency_injector import containers, providers

from src.core.infrastructure.repositories.user_repository import UserRepository
from src.core.application.services.user_service import UserService
from src.core.application.handlers.user.create_user_handler import CreateUserHandler
from src.core.application.handlers.user.get_user_by_id_handler import GetUserByIdHandler
from src.core.application.handlers.user.get_users_handler import GetUsersHandler
from src.core.application.handlers.user.deactivate_user_handler import DeactivateUserHandler
from src.core.application.handlers.user.update_user_handler import UpdateUserHandler
from src.core.application.handlers.user.delete_user_handler import DeleteUserHandler
from src.core.application.handlers.user.change_password_handler import ChangePasswordHandler


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

    get_user_by_id_handler = providers.Factory(
        GetUserByIdHandler,
        user_service=user_service
    )

    get_users_handler = providers.Factory(
        GetUsersHandler,
        user_service=user_service
    )

    deactivate_user_handler = providers.Factory(
        DeactivateUserHandler,
        user_service=user_service
    )

    update_user_handler = providers.Factory(
        UpdateUserHandler,
        user_service=user_service
    )

    delete_user_handler = providers.Factory(
        DeleteUserHandler,
        user_service=user_service
    )

    change_password_handler = providers.Factory(
        ChangePasswordHandler,
        user_service=user_service
    )