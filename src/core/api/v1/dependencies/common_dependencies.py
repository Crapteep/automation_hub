from fastapi import Depends, HTTPException, status
from typing import Annotated
from datetime import datetime, timezone
from pydantic import ValidationError

from src.core.application.services.user_service import UserService
from src.core.application.services.auth_service import AuthService
from src.core.domain.models.user import User
from src.core.domain.models.auth import TokenPayload
from src.core.infrastructure.containers.common_container import AutomationHubContainer
from jose import JWTError
from dependency_injector.wiring import Provide, inject
from src.core.api.v1.dependencies.auth_dependencies import oauth2_scheme

# Depends
TokenDep = Annotated[str, Depends(oauth2_scheme)]
UserServiceDep = Annotated[UserService, Depends(Provide[AutomationHubContainer.users.user_service])]
AuthServiceDep = Annotated[AuthService, Depends(Provide[AutomationHubContainer.auth.auth_service])]

@inject
async def get_current_user(
    token: TokenDep,
    user_service: UserServiceDep,
    auth_service: AuthServiceDep,
) -> User:
    try:
        payload = await auth_service.decode_token(token)
        print(payload)
        if not isinstance(payload, dict):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    if token_data.exp is not None:
        now = datetime.now(timezone.utc).timestamp()
        if now > token_data.exp:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
            )

    user = await user_service.get_user_by_id(user_id=token_data.sub)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    return user

CurrentUser = Annotated[User, Depends(get_current_user)]

async def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return current_user

CurrentSuperuser = Annotated[User, Depends(get_current_active_superuser)]