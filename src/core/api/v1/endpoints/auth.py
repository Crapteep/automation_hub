from fastapi import APIRouter, Depends
from src.core.application.commands.auth.login_user_command import LoginUserCommandResponse, LoginUserCommandRequest
from dependency_injector.wiring import inject
from src.core.decorators.exception_handler import handle_exceptions
from typing import Annotated
from src.core.api.v1.dependencies.auth_dependencies import LoginUserHandlerDep
from fastapi.security import OAuth2PasswordRequestForm


tags = [
    {
        "name": "Authentication",
        "description": "Endpoints related to authentication.",
    }
]

router = APIRouter(
    tags=["Authentication"],
)


@router.post("/login/access-token",
             response_model=LoginUserCommandResponse)
@inject
@handle_exceptions
async def login_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    handler: LoginUserHandlerDep
) -> LoginUserCommandResponse:
    command_request = LoginUserCommandRequest(
        email=form_data.username,
        password=form_data.password
    )
    return await handler(command_request)



@router.post("/logout")
async def logut_user():
    ...

@router.post("/token/refresh")
async def refresh_access_token():
    ...

@router.post("/login/verify")
async def verify_login_code():
    ...

@router.post("/password/forgot")
async def forgot_password():
    ...

@router.post("/password/reset")
async def reset_password():
    ...