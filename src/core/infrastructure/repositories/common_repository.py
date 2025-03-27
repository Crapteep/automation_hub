from sqlalchemy.ext.asyncio import AsyncSession

from typing import Protocol, Optional, Sequence, AsyncIterable
from pydantic import BaseModel, Field
from sqlmodel import select
from src.core.domain.models.user import User


class NotFound(Exception):
    ...

class AlreadyExists(Exception):
    ...


class RepositoryFilters(BaseModel):
    order: str | Sequence[str] | None = None
    page: int = Field(default=1, ge=1)
    size: int = Field(default=50, ge=1, le=100)

    def get_page_span_indexes(self) -> tuple[int, int]:
        span_start = (self.page - 1) * self.size
        span_end = span_start + self.size

        return span_start, span_end


class FetchRepository[RecordTypeOut, RecordIdTypeIn](Protocol):
    async def fetch(self, record_id: RecordIdTypeIn) -> RecordTypeOut:
        ...
    
class FetchManyRepository[RecordTypeOut, RecordIdTypeOut, FilterType](Protocol):
    async def fetch_many(self, filters: FilterType | None = None) -> tuple[int, AsyncIterable[RecordTypeOut]]:
        ...

class CreateRepository[RecordTypeIn, RecordIdTypeOut](Protocol):
    async def create(self, record: RecordTypeIn) -> RecordIdTypeOut:
        ...

class CreateManyRepository[RecordTypeIn, RecordIdTypeOut](Protocol):
    async def create_many(self, records: Sequence[RecordTypeIn]) -> Sequence[RecordIdTypeOut]:
        ...

class UpdateRepository[RecordTypeIn](Protocol):
    async def update(self, record: RecordTypeIn) -> None:
        ...
    
class UpdateOrCreateRepository[RecordTypeIn](Protocol):
    async def update_or_create(self, record: RecordTypeIn) -> bool:
        ...


class GenericRepository[
    RecordType,
    RecordIdType,
    FilterType,
](
    CreateRepository[RecordType, RecordIdType],
    CreateManyRepository[RecordType, RecordIdType],
    FetchRepository[RecordType, RecordIdType],
    FetchManyRepository[RecordType, RecordIdType, FilterType],
    UpdateRepository[RecordType],
    UpdateOrCreateRepository[RecordType],
    Protocol[RecordType, RecordIdType, FilterType]
):
    ...


class BaseRepository[
    RecordType,
    RecordIdType,
    FilterType](
        GenericRepository[
            RecordType,
            RecordIdType,
            FilterType
            ]
        ):
    
    allowed_models = {User}

    def __init__(self, model: type[RecordType], db: AsyncSession):
        if model not in self.allowed_models:
            raise TypeError(f"{model.__name__} is not allowed!")
        self.db = db
        self.model = model
    
    async def create(self, record: RecordType) -> RecordIdType:
        """Creates a new record and returns its ID."""
        self.db.add(record)
        await self.db.commit()
        await self.db.refresh(record)
        return record.id
    

    async def create_many(self, records: Sequence[RecordType]) -> Sequence[int]:
        """Creates multiple records at once."""
        self.db.add_all(records)
        await self.db.commit()
        return [record.id for record in records]
    

    async def fetch(self, record_id: RecordIdType) -> RecordType | None:
        """Retrieves the record by ID."""
        return await self.db.get(self.model, record_id)
    

    async def fetch_many(self, filters: FilterType | None = None) -> tuple[int, Sequence[RecordType]]:
        """Retrieves multiple records with filtering capabilities."""
        query = select(self.model)

        if filters:
            for field, value in filters.dict(exclude_none=True).items():
                query = query.where(getattr(self.model, field) == value)
        
        result = await self.db.execute(query)
        items = result.scalars().all()
        return len(items), items
    

    async def update(self, record: RecordType) -> None:
        """Updates an existing record."""
        self.db.add(record)
        await self.db.commit()
    

    async def update_or_create(self, record: RecordType) -> bool:
        """Updates the record if it exists, otherwise creates a new one."""
        existing_record = await self.fetch(record.id)
        if existing_record:
            self.db.add(record)
            await self.db.commit()
            return True
        else:
            await self.create(record)
            return False