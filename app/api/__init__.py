from fastapi import APIRouter, FastAPI

from app.api.admin.handlers import router as admin_router
from app.api.auth.handlers import router as auth_router
from app.api.card.handlers import router as card_router
from app.api.orders.handlers import router as order_router
from app.api.promotions.handlers import router as promotion_router
from app.api.srv.handlers import router as srv_router
from app.api.station.handlers import router as station_router
from app.api.token.handlers import router as token_router
from app.api.user.handlers import router as user_router

API_V1_PREFIX = "/api/v1"

root_router = APIRouter(prefix=API_V1_PREFIX)
root_router.include_router(auth_router)
root_router.include_router(user_router)
root_router.include_router(station_router)
root_router.include_router(order_router)
root_router.include_router(card_router)
root_router.include_router(promotion_router)
root_router.include_router(token_router)
root_router.include_router(admin_router)


def init_router(app: FastAPI) -> None:
    app.include_router(root_router)
    app.include_router(srv_router)
