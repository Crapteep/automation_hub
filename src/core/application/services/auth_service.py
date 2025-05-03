from src.core.infrastructure.repositories.user_repository import UserRepository
from src.core.application.commands.auth.login_user_command import LoginUserCommandRequest
from src.core.domain.exceptions.auth import InvalidCredentialsError
from src.core.domain.exceptions.user import InactiveUserError
from src.core.infrastructure.security.password import verify_password
from typing import Optional
from datetime import timedelta
from config.settings import Settings
from datetime import datetime, timedelta
from jose import JWTError, jwt
from config.settings import Settings
from datetime import datetime, timedelta, timezone
from typing import Any


settings = Settings()

class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    async def authenticate(self, command: LoginUserCommandRequest):
        user = await self.user_repository.fetch_by_email(email=command.email)
        if not user or not verify_password(command.password, user.hashed_password):
            raise InvalidCredentialsError("The login credentials entered are not valid")
        
        if not user.is_active:
            raise InactiveUserError("Inactive user")
        return user

    async def create_access_token(self, subject: str | Any, expires_delta: Optional[timedelta] = None) -> str:
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=self.access_token_expire_minutes))
        to_encode = {"exp": expire, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    async def decode_token(self, token: str) -> dict[str, Any] | None:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            exp = payload.get("exp")
            if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(timezone.utc):
                return None
            return payload
        except JWTError:
            return None


