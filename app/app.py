from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api import init_router
from app.api.errors.handlers import register_exception_handlers
from app.dependencies.web_app import WebAppContainer
from app.infrastructure.logging import setup_logging
from app.persistent.db_schemas import init_mappers


async def start_collector_expired_payments(container: WebAppContainer) -> None:
    cron_collector_expired_payments = container.cron_collector_expired_sessions()
    await cron_collector_expired_payments.startup()


def init_middlewares(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
    )


def create_app() -> FastAPI:
    container = WebAppContainer()
    settings = container.settings()
    setup_logging(settings.logging)

    async def on_startup() -> None:
        init_mappers()

        resources = container.init_resources()
        if resources is None:
            raise ValueError("Expected an awaitable, got None")
        await resources

    async def on_shutdown() -> None:
        shutdown_res = container.shutdown_resources()
        if shutdown_res is None:
            raise ValueError("Expected an awaitable, got None")
        await shutdown_res

    app = FastAPI(title=settings.srv.app_name, version="0.1.0", on_startup=[on_startup], on_shutdown=[on_shutdown])
    init_middlewares(app=app)
    init_router(app)
    register_exception_handlers(app)

    return app
