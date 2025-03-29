from fastapi import APIRouter, FastAPI

from app.api.admin.handlers import router as admin_router
from app.api.auth.handlers import router as auth_router
from app.api.token.handlers import router as token_router
from app.api.user.handlers import router as user_router

API_V1_PREFIX = "/api"

root_router = APIRouter(prefix=API_V1_PREFIX)
root_router.include_router(auth_router)
root_router.include_router(user_router)
root_router.include_router(token_router)
root_router.include_router(admin_router)


def init_router(app: FastAPI) -> None:
    app.include_router(root_router)
