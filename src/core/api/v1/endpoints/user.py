from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Query, Depends, Body, Path





tags = [
    {
        "name": "Users",
        "description": "Endpoints related to Users.",
    }
]

router = APIRouter(
    tags=["Users"],
)


@router.get("/")
# @inject
async def root():
    return {"message": "test"}