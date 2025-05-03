
from src.core.infrastructure.repositories.user_repository import UserRepository
from src.core.domain.models.user import CreateUserDBData, UserResponse, User
from src.core.application.commands.user.create_user_command import CreateUserCommandRequest
from src.core.application.queries.user.get_users_query import GetUsersQueryRequest
from src.core.application.commands.user.change_password_comand import ChangePasswordCommandRequest
from src.core.application.commands.user.update_user_command import (
    UpdateUserCommandRequest,
    UpdateCurrentUserCommandRequest
)
from src.core.domain.exceptions.user import (
    InvalidUserDataError,
    UserAlreadyExistsError,
    UserNotFoundError,
    UsersNotFoundError,
    UserAlreadyInactiveError,
    EmailAlreadyTakenError,
    UsernameAlreadyTakenError,
    NoPermissionError,
    InvalidPasswordError,
    PasswordReuseError
)

from src.core.infrastructure.security.password import get_password_hash, verify_password
from uuid import UUID
from datetime import datetime, timezone


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    

    async def create_user(self, command: CreateUserCommandRequest) -> None:
        """Create a new user based on the provided command.

        Args:
            command: The command containing user creation data (username, email, password).

        Raises:
            UserAlreadyExistsError: If a user with the given email already exists.
            InvalidUserDataError: If the provided data is invalid (e.g., empty username).
        """
        if not command.username.strip():
            raise InvalidUserDataError("Username cannot be empty")
        
        if command.username.lower() in {"admin", "root"}:
            raise InvalidUserDataError("Username is reserved and cannot be used")
        
        existing_user_by_username = await self.user_repository.fetch_by_username(username=command.username)
        if existing_user_by_username:
            raise UserAlreadyExistsError(f"User with this username {command.username} already exists")

        existing_user_by_email = await self.user_repository.fetch_by_email(email=command.email)
        if existing_user_by_email:
            raise UserAlreadyExistsError(f"User with email {command.email} already exists")

        user_data = CreateUserDBData(
            username=command.username,
            email=command.email,
            hashed_password=get_password_hash(command.password)
        )

        return await self.user_repository.create(user_data)
    

    async def get_user_by_id(self, user_id: UUID) -> UserResponse | None:
        """Fetch a user by their ID.

        Args:
            user_id: The UUID of the user to fetch.

        Returns:
            The User object if found, else None.
        """
        user = await self.user_repository.fetch_by_id(record_id=user_id)
        if not user: 
            raise UserNotFoundError(f"User with ID {user_id} does not exist.")
        

        return UserResponse.model_validate(user)
    
    
    async def get_users(self, query: GetUsersQueryRequest) -> list[UserResponse]:
        users = await self.user_repository.fetch_all_filtered(query=query)
        if not users:
            raise UsersNotFoundError("No users found.")
        return [UserResponse.model_validate(user) for user in users]


    async def deactivate_user(self, user_id: UUID) -> None:
        user = await self.user_repository.fetch_by_id(record_id=user_id)
        if not user:
            raise UserNotFoundError(f"User with ID {user_id} does not exist.")
        
        if not user.is_active:
            raise UserAlreadyInactiveError("User is already inactive.")
        
        user.is_active = False
        await self.user_repository.update(record=user)


    async def update_user(self,
                          user_id: UUID,
                          data: UpdateUserCommandRequest
                          ) -> bool:
        user = await self.user_repository.fetch_by_id(record_id=user_id)
        if not user:
            raise UserNotFoundError(f"User with ID {user_id} does not exist.")
        
        if not user.is_active and isinstance(data, UpdateCurrentUserCommandRequest):
            raise UserAlreadyInactiveError("User is already inactive.")
        
        update_data = data.model_dump(exclude_unset=True)

        if isinstance(data, UpdateCurrentUserCommandRequest):
            update_data.pop("is_active", None)
            update_data.pop("is_superuser", None)

        if "email" in update_data and update_data["email"] != user.email:
            existing_user = await self.user_repository.fetch_by_email(email=update_data["email"])
            if existing_user and existing_user.id != user.id:
                raise EmailAlreadyTakenError("This email is already in use.")
        
        if "username" in update_data and update_data["username"] != user.username:
            existing_user = await self.user_repository.fetch_by_username(username=update_data["username"])
            if existing_user and existing_user.id != user.id:
                raise UsernameAlreadyTakenError("This username is already in use.")


        for key, value in update_data.items():
            setattr(user, key, value)
        
        await self.user_repository.update(record=user)
        return True
    
    async def delete_user(self, user_id: UUID) -> bool:
        user = await self.user_repository.fetch_by_id(record_id=user_id)

        if not user:
            raise UserNotFoundError(f"User with ID {user_id} does not exist.")
        
        if not user.is_active:
            raise UserAlreadyInactiveError("User is already inactive and cannot be deleted.")
        
        if user.is_superuser:
            raise NoPermissionError("No sufficient permissions to delete a user")
        
        return await self.user_repository.delete(record_id=user_id)
    

    async def change_user_password(self, user_id: UUID, command: ChangePasswordCommandRequest):
        user: User = await self.user_repository.fetch_by_id(record_id=user_id)

        if not user:
            raise UserNotFoundError(f"User with ID {user_id} does not exist.")
        
        if not verify_password(command.old_password, user.hashed_password):
            raise InvalidPasswordError("Old password is incorrect.")
        
        if verify_password(command.new_password, user.hashed_password):
            raise PasswordReuseError("New password must be different from the old password.")
        
        user.hashed_password = get_password_hash(command.new_password)
        await self.user_repository.update(user)