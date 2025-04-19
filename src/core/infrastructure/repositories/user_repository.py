
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from src.core.infrastructure.repositories.common_repository import BaseRepository, RepositoryFilters
from src.core.domain.exceptions.user import UserAlreadyExistsError
from src.core.domain.models.user import User
from src.core.infrastructure.database.db import Database
from uuid import UUID

class UserFilters(RepositoryFilters):
    username: str | None = None
    email: str | None = None


class UserRepository(BaseRepository[User, UUID, UserFilters]):
    def __init__(self, db: Database):
        super().__init__(User, db)
    
    async def fetch_by_email(self, session: AsyncSession, email: str) -> User | None:
        """Retrieves a user by their email.

        Args:
            session: The async database session.
            email: The email of the user to fetch.

        Returns:
            The User object if found, else None.
        """
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        return result.first()
    
    def _map_integrity_error(self, error: IntegrityError) -> Exception:
        """Map IntegrityError to UserAlreadyExistsError for unique constraint violations."""
        if "unique constraint" in str(error).lower():
            return UserAlreadyExistsError("User with this email or username already exists")
        return error
