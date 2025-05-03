
#commands
from src.core.application.commands.user.create_user_command import CreateUserCommandRequest, CreateUserCommandResponse
from src.core.application.commands.user.delete_user_command import DeleteUserCommandRequest, DeleteUserCommandResponse
from src.core.application.commands.user.deactivate_user_command import DeactivateUserCommandRequest, DeactivateUserCommandResponse
from src.core.application.commands.user.update_user_command import (
    UpdateCurrentUserCommandRequest,
    UpdateCurrentUserCommandResponse,
    UpdateUserByAdminCommandRequest,
    UpdateUserByAdminCommandResponse
)
from src.core.application.commands.user.change_password_comand import ChangePasswordCommandRequest, ChangePasswordCommandResponse
#queries
from src.core.application.queries.user.get_user_by_id_query import GetUserByIdQueryRequest, GetUserByIdQueryResponse
from src.core.application.queries.user.get_users_query import GetUsersQueryRequest, GetUsersQueryResponse

#deps
from src.core.api.v1.dependencies.common_dependencies import CurrentUser, CurrentSuperuser
from src.core.api.v1.dependencies.user_dependencies import (
    GetUserByIdHandlerDep,
    CreateUserHandlerDep,
    GetUsersHandlerDep,
    DeactivateUserHandlerDep,
    UpdateUserHandlerDep,
    DeleteUserHandlerDep,
    ChangePasswordHandlerDep,
)
from src.core.domain.exceptions.user import (
    UserAlreadyExistsError,
    UserNotFoundError,
    InvalidUserDataError,
    UsersNotFoundError,
    UserAlreadyInactiveError,
    NoPermissionError,
    InvalidPasswordError,
    PasswordReuseError,
)

from src.core.domain.models.user import UserResponse, UserId
from src.core.decorators.exception_handler import handle_exceptions
from src.utils.utils import generate_openapi_responses

from fastapi import APIRouter, Body, Query
from typing import Annotated
from dependency_injector.wiring import inject


tags = [
    {
        "name": "Users",
        "description": "Endpoints related to Users.",
    }
]

router = APIRouter(
    tags=["Users"],
    prefix="/users"
)

@handle_exceptions
@router.get("/me",
            response_model=UserResponse)
async def read_users_me(current_user: CurrentUser) -> UserResponse:
    """Get current user details."""
    return UserResponse.model_validate(current_user)


@router.post("/",
             response_model=CreateUserCommandResponse,
             responses=generate_openapi_responses(UserAlreadyExistsError, InvalidUserDataError))
@inject
@handle_exceptions
async def create_user(
    command_request: Annotated[CreateUserCommandRequest, Body()],
    handler: CreateUserHandlerDep,
    current_superuser: CurrentSuperuser
) -> CreateUserCommandResponse:
    return await handler(command_request)


@router.get("/{user_id}",
            response_model=GetUserByIdQueryResponse,
            responses=generate_openapi_responses(UserNotFoundError))
@inject
@handle_exceptions
async def get_user(
    user_id: UserId,
    handler: GetUserByIdHandlerDep,
    current_superuser: CurrentSuperuser
 ) -> GetUserByIdQueryResponse:
    query = GetUserByIdQueryRequest(user_id=user_id)
    return await handler(query)


@router.get("/",
            response_model=GetUsersQueryResponse,
            responses=generate_openapi_responses(UsersNotFoundError)
            )
@inject
@handle_exceptions
async def get_users(
    query_request: Annotated[GetUsersQueryRequest, Query()],
    handler: GetUsersHandlerDep,
    current_superuser: CurrentSuperuser
) -> GetUsersQueryResponse:
    return await handler(query_request)



@router.delete("/me",
               response_model=DeactivateUserCommandResponse,
               responses=generate_openapi_responses(UserAlreadyInactiveError, UserNotFoundError))
@inject
@handle_exceptions
async def deactivate_current_user(
    handler: DeactivateUserHandlerDep,
    current_user: CurrentUser
) -> DeactivateUserCommandResponse:
    command_request = DeactivateUserCommandRequest(user_id=current_user.id)
    return await handler(command_request)



@router.patch("/me",
              response_model=UpdateCurrentUserCommandResponse,
              responses=generate_openapi_responses(UserNotFoundError, UserAlreadyInactiveError))
@inject
@handle_exceptions
async def update_user(
    command_request: Annotated[UpdateCurrentUserCommandRequest, Body()],
    handler: UpdateUserHandlerDep,
    current_user: CurrentUser
) -> UpdateCurrentUserCommandResponse:
    return await handler(user_id=current_user.id, command=command_request)


@router.patch("/{user_id}",
              response_model=UpdateUserByAdminCommandResponse,
              responses=generate_openapi_responses(UserNotFoundError, UserAlreadyInactiveError))
@inject
@handle_exceptions
async def update_user_by_admin(
    user_id: UserId,
    command_request: Annotated[UpdateUserByAdminCommandRequest, Body()],
    handler: UpdateUserHandlerDep,
    current_superuser: CurrentSuperuser
) -> UpdateUserByAdminCommandResponse:
    return await handler(user_id=user_id, command=command_request)


@router.post("/me/change-password",
             response_model=ChangePasswordCommandResponse,
             responses=generate_openapi_responses(InvalidPasswordError, UserNotFoundError, PasswordReuseError))
@inject
@handle_exceptions
async def change_own_password(
    command_request: Annotated[ChangePasswordCommandRequest, Body()],
    handler: ChangePasswordHandlerDep,
    current_user: CurrentUser
) -> ChangePasswordCommandResponse:
    return await handler(user_id=current_user.id, command=command_request)



@router.delete("/{user_id}",
               response_model=DeleteUserCommandResponse,
               responses=generate_openapi_responses(UserAlreadyInactiveError, NoPermissionError, UserNotFoundError))
@inject
@handle_exceptions
async def delete_user(
    user_id: UserId,
    reason: Annotated[str, Query(..., description="Reason for delection")],
    handler: DeleteUserHandlerDep,
    current_superuser: CurrentSuperuser
) -> DeleteUserCommandResponse:
    command_request = DeleteUserCommandRequest(user_id=user_id, reason=reason)
    return await handler(command_request)



