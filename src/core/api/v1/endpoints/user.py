from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Query, Depends, Body, Path, HTTPException
from src.core.application.commands.user.create_user_command import CreateUserCommandRequest, CreateUserCommand, CreateUserCommandResponse
from src.core.application.handlers.user.create_user_handler import CreateUserHandler, CommandExecutionError
from src.core.infrastructure.containers.common_container import AutomationHubContainer
from src.core.domain.exceptions.user import UserAlreadyExistsError



tags = [
    {
        "name": "Users",
        "description": "Endpoints related to Users.",
    }
]

router = APIRouter(
    tags=["Users"],
)


@router.post("/")
@inject
async def create_user(
    command_request: Annotated[CreateUserCommandRequest, Body()],
    handler: CreateUserHandler = Depends(Provide[AutomationHubContainer.users.create_user_handler])
) -> CreateUserCommandResponse:
    try:
        return await handler(command_request)
    except CommandExecutionError as e:
        if isinstance(e.cause, UserAlreadyExistsError):
            raise HTTPException(status_code=409, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}")
async def get_user():
    pass