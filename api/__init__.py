from fastapi import APIRouter

from .v1.routes import api_router


router = APIRouter(
    prefix="/api"
)

router.include_router(api_router)
