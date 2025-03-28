from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from src.core.infrastructure.repositories.common_repository import BaseRepository, RepositoryFilters
from src.core.domain.models.user import User
from uuid import UUID

class UserFilters(RepositoryFilters):
    username: str | None = None
    email: str | None = None


class UserRepository(BaseRepository[User, UUID, UserFilters]):
    def __init__(self, db: AsyncSession):
        super().__init__(User, db)
