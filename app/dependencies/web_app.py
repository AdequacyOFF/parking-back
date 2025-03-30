from aioboto3 import Session
from aioredis import Redis
from dependency_injector import containers, providers

from app.infrastructure.db import Database, SessionContext
from app.infrastructure.redis import RedisDatabaseType, init_redis_pool
from app.repositories.uow import UnitOfWork
from app.settings import Settings
from app.use_cases.admin.auth import AdminAuthUseCase
from app.use_cases.admin.refresh import AdminTokenRefreshUseCase
from app.use_cases.admin.delete_user import UserDeleteUseCase
from app.use_cases.admin.register_user import UserRegisterUseCase
from app.use_cases.auth.logout import LogoutUseCase
from app.use_cases.token.refresh import RefreshUseCase
from app.use_cases.user.auth import UserAuthUseCase
from app.use_cases.user.change_user import ChangeUserUseCase
from app.use_cases.place.create_parking import ParkingCreateUseCase
from app.use_cases.place.assign_place import PlaceAssignUseCase
from app.views.user.me import GetUserView

# from app.workers.account.account_update import CronAccountUpdatedHandler, init_cron_account_handler


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

    user_auth_use_case: providers.Factory[UserAuthUseCase] = providers.Factory(UserAuthUseCase, uow=unit_of_work)
    # auth_init_use_case: providers.Factory[InitUseCase] = providers.Factory(
    #     InitUseCase,
    #     uow=unit_of_work,
    #     settings=settings,
    # )
    user_delete_use_case = providers.Factory(UserDeleteUseCase, uow=unit_of_work)
    user_register_use_case = providers.Factory(UserRegisterUseCase, uow=unit_of_work)
    user_change_user = providers.Factory(ChangeUserUseCase, uow=unit_of_work)
    parking_create_use_case = providers.Factory(ParkingCreateUseCase, uow=unit_of_work)

    token_refresh_use_case = providers.Factory(RefreshUseCase, uow=unit_of_work)
    auth_logout_use_case = providers.Factory(LogoutUseCase, uow=unit_of_work)
    place_assign_use_case = providers.Factory(PlaceAssignUseCase, uow=unit_of_work)
    # Views
    user_get_user_view = providers.Factory(GetUserView, uow=unit_of_work)
