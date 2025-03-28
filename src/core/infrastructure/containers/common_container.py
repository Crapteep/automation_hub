import inspect
import logging.config
from contextlib import asynccontextmanager
from typing import ParamSpec, TypeVar, AsyncIterator
from src.core.infrastructure.database.db import Database
from src.core.infrastructure.repositories.user_repository import UserRepository
from config.settings import Settings

from dependency_injector import containers, providers

logger = logging.getLogger(__name__)

P = ParamSpec("P")
R = TypeVar("R")


@asynccontextmanager
async def initialized_resources(
    container: containers.DeclarativeContainer,
) -> AsyncIterator[None]:
    
    await container.db().init_db()

    init_resources = container.init_resources()
    if inspect.isawaitable(init_resources):
        await init_resources
    
    yield

    shutdown_resources = container.shutdown_resources()
    if inspect.isawaitable(shutdown_resources):
        await shutdown_resources

    await container.db().shutdown()


class AutomationHubContainer(containers.DeclarativeContainer):
    """Main application container"""
    wiring_config = containers.WiringConfiguration(
        modules=["src.main"]
    )

    settings = providers.Configuration()

    configure_logging = providers.Callable(
        logging.config.dictConfig,
        settings.logging_dict,
    )


    #db connection
    db = providers.Singleton(Database, db_url=settings.db_url)

    #Repositories
    user_repository = providers.Factory(UserRepository, db=db)


    #Services
    



def create_container() -> AutomationHubContainer:
    container = AutomationHubContainer()
    container.settings.from_pydantic(Settings())

    return container