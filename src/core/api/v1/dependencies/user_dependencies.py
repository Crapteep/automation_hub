from fastapi import Depends
from dependency_injector.wiring import Provide
from src.core.infrastructure.containers.user_container import UserContainer
from src.core.application.handlers.user.create_user_handler import CreateUserHandler
from src.core.application.handlers.user.get_user_by_id_handler import GetUserByIdHandler
from src.core.application.handlers.user.get_users_handler import GetUsersHandler
from src.core.application.handlers.user.deactivate_user_handler import DeactivateUserHandler
from src.core.application.handlers.user.update_user_handler import UpdateUserHandler
from src.core.application.handlers.user.delete_user_handler import DeleteUserHandler
from src.core.application.handlers.user.change_password_handler import ChangePasswordHandler
from typing import Annotated
from src.core.infrastructure.containers.common_container import AutomationHubContainer


CreateUserHandlerDep = Annotated[CreateUserHandler, Depends(Provide[AutomationHubContainer.users.create_user_handler])]
GetUserByIdHandlerDep = Annotated[GetUserByIdHandler, Depends(Provide[AutomationHubContainer.users.get_user_by_id_handler])]
GetUsersHandlerDep = Annotated[GetUsersHandler, Depends(Provide[AutomationHubContainer.users.get_users_handler])]
DeactivateUserHandlerDep = Annotated[DeactivateUserHandler, Depends(Provide[AutomationHubContainer.users.deactivate_user_handler])]
UpdateUserHandlerDep = Annotated[UpdateUserHandler, Depends(Provide[AutomationHubContainer.users.update_user_handler])]
DeleteUserHandlerDep = Annotated[DeleteUserHandler, Depends(Provide[AutomationHubContainer.users.delete_user_handler])]
ChangePasswordHandlerDep = Annotated[ChangePasswordHandler, Depends(Provide[AutomationHubContainer.users.change_password_handler])]