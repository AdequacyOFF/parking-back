from aioboto3 import Session
from aioredis import Redis
from dependency_injector import containers, providers

from app.infrastructure.db import Database, SessionContext
from app.infrastructure.redis import RedisDatabaseType, init_redis_pool
from app.repositories.uow import UnitOfWork
from app.settings import Settings
from app.use_cases.admin.auth import AdminAuthUseCase
from app.use_cases.admin.refresh import AdminTokenRefreshUseCase
from app.use_cases.auth.init import InitUseCase
from app.use_cases.auth.logout import LogoutUseCase
from app.use_cases.auth.verify import VerifyUseCase
from app.use_cases.token.refresh import RefreshUseCase
from app.use_cases.user.change_user import ChangeUserUseCase
from app.use_cases.user.delete_user import DeleteUserUseCase
from app.use_cases.user.register import RegisterUseCase
from app.views.user.get_fcm_token import GetFCMTokenView
from app.views.user.me import GetUserView


class WebAppContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["app.api", __name__])
    settings = providers.Singleton(Settings)
    database: providers.Provider[Database] = providers.Singleton(Database, settings.provided.database)
    otp_redis: providers.Resource[Redis] = providers.Resource(
        init_redis_pool, settings=settings.provided.redis, db=RedisDatabaseType.OTP
    )

    boto_session: providers.Singleton[Session] = providers.Singleton(Session)

    session_context = providers.Factory(SessionContext)

    unit_of_work = providers.ContextLocalSingleton(
        UnitOfWork, session_context=session_context, database=database, otp_redis=otp_redis
    )

    # Use Cases
    admin_auth_use_case: providers.Factory[AdminAuthUseCase] = providers.Factory(AdminAuthUseCase, uow=unit_of_work)
    admin_token_refresh_use_case: providers.Factory[AdminTokenRefreshUseCase] = providers.Factory(
        AdminTokenRefreshUseCase, uow=unit_of_work
    )

    auth_init_use_case: providers.Factory[InitUseCase] = providers.Factory(
        InitUseCase,
        uow=unit_of_work,
        settings=settings,
    )
    auth_verify_use_case = providers.Factory(VerifyUseCase, uow=unit_of_work)
    auth_logout_use_case = providers.Factory(LogoutUseCase, uow=unit_of_work)
    delete_user_use_case = providers.Factory(DeleteUserUseCase, uow=unit_of_work)
    user_register_use_case = providers.Factory(RegisterUseCase, uow=unit_of_work)
    user_change_user = providers.Factory(ChangeUserUseCase, uow=unit_of_work)
    token_refresh_use_case = providers.Factory(RefreshUseCase, uow=unit_of_work)

    # Views
    user_get_user_view = providers.Factory(GetUserView, uow=unit_of_work)
    user_get_fcm_token_view = providers.Factory(GetFCMTokenView, uow=unit_of_work)
