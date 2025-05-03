from fastapi import Depends
from typing import Annotated
from dependency_injector.wiring import Provide
from src.core.infrastructure.containers.user_container import UserContainer
from src.core.application.handlers.auth.login_user_handler import LoginUserHandler
from src.core.infrastructure.containers.common_container import AutomationHubContainer
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/login/access-token")

LoginUserHandlerDep = Annotated[LoginUserHandler, Depends(Provide[AutomationHubContainer.auth.login_user_handler])]
