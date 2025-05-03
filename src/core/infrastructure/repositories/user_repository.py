
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, asc, desc
from sqlalchemy.exc import IntegrityError
from src.core.infrastructure.repositories.common_repository import BaseRepository, RepositoryFilters
from src.core.domain.exceptions.user import UserAlreadyExistsError
from src.core.domain.models.user import User
from src.core.infrastructure.database.db import Database
from src.core.application.queries.user.get_users_query import GetUsersQueryRequest
from uuid import UUID
from src.core.infrastructure.repositories.common_repository import with_session

class UserFilters(RepositoryFilters):
    username: str | None = None
    email: str | None = None


class UserRepository(BaseRepository[User, UUID, UserFilters]):
    def __init__(self, db: Database):
        super().__init__(User, db)
    
    @with_session
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
    

    @with_session
    async def fetch_by_username(self, session: AsyncSession, username: str) -> User | None:
        statement = select(User).where(User.username == username)
        result = await session.exec(statement)
        return result.first()
    
    @with_session
    async def fetch_all_filtered(
        self,
        session: AsyncSession,
        query: GetUsersQueryRequest
    ) -> list[User]:
        stmt = select(User)

        if query.search:
            stmt = stmt.where(User.email.ilike(f"%{query.search}%"))
        
        if query.is_active is not None:
            stmt = stmt.where(User.is_active == query.is_active)
        
        if query.is_superuser is not None:
            stmt =stmt.where(User.is_superuser == query.is_superuser)

        if query.sort_by and hasattr(User, query.sort_by):
            column = getattr(User, query.sort_by)
            stmt = stmt.order_by(asc(column) if query.sort_order == "asc" else desc(column))
        
        stmt = stmt.offset(query.skip).limit(query.limit)

        result = await session.exec(stmt)
        users = result.all()
        return users
                                 
    
    def _map_integrity_error(self, error: IntegrityError) -> Exception:
        """Map IntegrityError to UserAlreadyExistsError for unique constraint violations."""
        if "unique constraint" in str(error).lower():
            return UserAlreadyExistsError("User with this email or username already exists")
        return error
