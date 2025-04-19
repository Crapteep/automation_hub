from typing import Any, Callable, Sequence, Optional, AsyncIterable, TypeVar, ParamSpec
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, Field
from functools import wraps
from src.core.infrastructure.database.db import Database
from typing import Protocol

class RepositoryFilters(BaseModel):
    order: str | Sequence[str] | None = None
    page: int = Field(default=1, ge=1)
    size: int = Field(default=50, ge=1, le=100)

    def get_page_span_indexes(self) -> tuple[int, int]:
        span_start = (self.page - 1) * self.size
        span_end = span_start + self.size
        return span_start, span_end

class GenericRepository[RecordType, RecordIdType, FilterType](Protocol):
    async def create(self, record: RecordType | BaseModel) -> RecordIdType:
        ...
    async def create_many(self, records: Sequence[RecordType | BaseModel]) -> Sequence[RecordIdType]:
        ...
    async def fetch(self, record_id: RecordIdType) -> RecordType | None:
        ...
    async def fetch_many(self, filters: FilterType | None = None) -> tuple[int, AsyncIterable[RecordType]]:
        ...
    async def update(self, record: RecordType) -> None:
        ...
    async def update_or_create(self, record: RecordType) -> bool:
        ...

P = ParamSpec("P")
R = TypeVar("R")

def with_session(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    async def wrapper(self: Any, *args: P.args, **kwargs: P.kwargs) -> R:
        if not hasattr(self, 'db'):
            raise AttributeError("Repository must have 'db' attribute")
        async with self.db.session() as session:
            try:
                if 'session' in func.__annotations__:
                    return await func(self, session, *args, **kwargs)
                return await func(self, *args, **kwargs)
            except Exception as e:
                await session.rollback()
                raise
    return wrapper

class BaseRepository[RecordType, RecordIdType, FilterType](GenericRepository[RecordType, RecordIdType, FilterType]):
    def __init__(self, model: type[RecordType], db: Database):
        from sqlmodel import SQLModel
        if not issubclass(model, SQLModel):
            raise TypeError(f"{model.__name__} must inherit from SQLModel")
        self.db = db
        self.model = model
    
    @with_session
    async def create(self, session: AsyncSession, record: RecordType | BaseModel) -> RecordIdType:
        """Creates a new record and returns its ID."""
        try:
            if isinstance(record, BaseModel):
                record = self.model(**record.dict())
            session.add(record)
            await session.commit()
            await session.refresh(record)
            return record.id
        except IntegrityError as e:
            await session.rollback()
            raise self._map_integrity_error(e) from e
    
    @with_session
    async def create_many(self, session: AsyncSession, records: Sequence[RecordType | BaseModel]) -> Sequence[RecordIdType]:
        """Creates multiple records at once."""
        try:
            records = [self.model(**record.dict()) if isinstance(record, BaseModel) else record for record in records]
            session.add_all(records)
            await session.commit()
            return [record.id for record in records]
        except IntegrityError as e:
            await session.rollback()
            raise self._map_integrity_error(e) from e
    
    @with_session
    async def fetch(self, session: AsyncSession, record_id: RecordIdType) -> RecordType | None:
        """Retrieves the record by ID."""
        return await session.get(self.model, record_id)
    
    @with_session
    async def fetch_many(self, session: AsyncSession, filters: FilterType | None = None) -> tuple[int, Sequence[RecordType]]:
        """Retrieves multiple records with filtering capabilities."""
        query = select(self.model)
        if filters:
            for field, value in filters.dict(exclude_none=True).items():
                if hasattr(self.model, field):
                    query = query.where(getattr(self.model, field) == value)
            if hasattr(filters, "page") and hasattr(filters, "size"):
                span_start, span_end = filters.get_page_span_indexes()
                query = query.offset(span_start).limit(filters.size)
        result = await session.exec(query)
        items = result.scalars().all()
        return len(items), items
    
    @with_session
    async def update(self, session: AsyncSession, record: RecordType) -> None:
        """Updates an existing record."""
        from datetime import datetime, timezone
        if hasattr(record, "updated_at"):
            record.updated_at = datetime.now(timezone.utc)
        session.add(record)
        await session.commit()
    
    @with_session
    async def update_or_create(self, session: AsyncSession, record: RecordType) -> bool:
        """Updates the record if it exists, otherwise creates a new one."""
        existing_record = await self.fetch(session, record.id)
        if existing_record:
            session.add(record)
            await session.commit()
            return True
        else:
            await self.create(session, record)
            return False
    
    def _map_integrity_error(self, error: IntegrityError) -> Exception:
        """Map IntegrityError to a domain-specific exception. Subclasses should override."""
        return Exception(f"Database integrity error: {error}")