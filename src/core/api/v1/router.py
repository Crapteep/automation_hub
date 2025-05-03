from fastapi import APIRouter
from .endpoints import user, auth

router = APIRouter()
router.include_router(user.router)
router.include_router(auth.router)