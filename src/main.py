from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import AsyncIterator
from dependency_injector.containers import DeclarativeContainer
from src.core.infrastructure.containers.common_container import initialized_resources, create_container
from src.core.api.v1.router import router as v1_router


class FastAPIWithContainer(FastAPI):
    container: DeclarativeContainer


@asynccontextmanager
async def lifespan(app: FastAPIWithContainer) -> AsyncIterator[None]:
    async with initialized_resources(app.container):
        yield


router = APIRouter(tags=["General"])


@router.get("/")
async def read_root() -> dict[str, str]:
    return {"version": "0.1.0"}

def create_app() -> FastAPI:
    container = create_container()
    container.configure_logging()
    

    settings = container.settings()

    app = FastAPIWithContainer(
        title=settings["title"],
        lifespan=lifespan,
        tags=[
            {
                "name": "General",
                "description": "General operations",
            },
            #tutaj dodać routers
        ]
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins = ["*"],
        allow_credentials = True,
        allow_methods = ["*"],
        allow_headers = ["*"],
    )

    app.container = container
    app.include_router(router)
    app.include_router(v1_router, prefix="/v1")

    return app


app = create_app()