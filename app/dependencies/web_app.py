from aioboto3 import Session
from aioredis import Redis
from dependency_injector import containers, providers

from app.adapters.card_master.adapter import CardMasterAdapter
from app.adapters.file_storage.adapter import FileStorageAdapter, IFileStorageAdapter
from app.adapters.mail.adapter import IMailAdapter, MailAdapter
from app.adapters.notifications.adapter import NotificationsAdapter
from app.adapters.telegram.adapter import TelegramNotificationsAdapter
from app.infrastructure.db import Database, SessionContext
from app.infrastructure.http_client.card_master.client import CardMasterHTTPClient
from app.infrastructure.http_client.enums import ClientsEnum
from app.infrastructure.http_client.factory import HttpClientsFactory
from app.infrastructure.http_client.notifications.client import NotificationsHTTPClient
from app.infrastructure.metrics import MetricClient
from app.infrastructure.redis import RedisDatabaseType, init_redis_pool
from app.infrastructure.smtp import ISmtpClient, SmtpClient
from app.repositories.uow import UnitOfWork
from app.settings import Settings
from app.use_cases.admin.auth import AdminAuthUseCase
from app.use_cases.admin.change_min_volume import ChangeMinFuelVolumeUseCase
from app.use_cases.admin.create_promotion import CreatePromotionUseCase
from app.use_cases.admin.delete_promotion import DeletePromotionUseCase
from app.use_cases.admin.refresh import AdminTokenRefreshUseCase
from app.use_cases.admin.update_promotion import UpdatePromotionUseCase
from app.use_cases.auth.init import InitUseCase
from app.use_cases.auth.logout import LogoutUseCase
from app.use_cases.auth.verify import VerifyUseCase
from app.use_cases.orders.create_order_request import CreateOrderRequestUseCase
from app.use_cases.orders.submit_feedback import SubmitFeedbackUseCase
from app.use_cases.token.refresh import RefreshUseCase
from app.use_cases.user.change_user import ChangeUserUseCase
from app.use_cases.user.delete_user import DeleteUserUseCase
from app.use_cases.user.register import RegisterUseCase
from app.use_cases.user.register_agreement import RegisterAgreementsUseCase
from app.views.card.get_card_bonuses import GetCardBonusesView
from app.views.card.get_card_info import GetCardInfoView
from app.views.orders.get_min_volume import GetMinFuelVolumeView
from app.views.orders.get_orders import GetOrdersView
from app.views.promotions.get_promotion import GetPromotionView
from app.views.promotions.get_promotions import GetPromotionsView
from app.views.stations.get_oils import GetOilsView
from app.views.stations.get_services import GetServicesView
from app.views.stations.get_stations import GetGasStationsView
from app.views.user.get_fcm_token import GetFCMTokenView
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
    # Clients
    client_factory: providers.Singleton[HttpClientsFactory] = providers.Singleton(HttpClientsFactory)
    notifications_client: providers.Singleton[NotificationsHTTPClient] = providers.Singleton(
        client_factory.provided(), client_name=ClientsEnum.NOTIFICATIONS
    )
    card_master_client: providers.Singleton[CardMasterHTTPClient] = providers.Singleton(
        client_factory.provided(), client_name=ClientsEnum.CARD_MASTER
    )
    smtp_client: providers.Singleton[ISmtpClient] = providers.Singleton(SmtpClient, settings=settings.provided.mail)
    telegram_notification_client: providers.Singleton[CardMasterHTTPClient] = providers.Singleton(
        client_factory.provided(), client_name=ClientsEnum.TELEGRAM_NOTIFICATION
    )
    # Adapters
    fs_adapter: providers.Singleton[IFileStorageAdapter] = providers.Singleton(
        FileStorageAdapter, boto_session=boto_session, settings=settings.provided.fs_settings
    )
    mail_adapter: providers.Singleton[IMailAdapter] = providers.Singleton(MailAdapter, client=smtp_client)
    notifications_adapter: providers.Singleton[NotificationsAdapter] = providers.Singleton(
        NotificationsAdapter, client=notifications_client
    )
    card_master_adapter: providers.Singleton[CardMasterAdapter] = providers.Singleton(
        CardMasterAdapter, client=card_master_client
    )
    telegram_notification_adapter: providers.Singleton[TelegramNotificationsAdapter] = providers.Singleton(
        TelegramNotificationsAdapter, client=telegram_notification_client
    )
    # Prometheus
    metric_manager: providers.Singleton[MetricClient] = providers.Singleton(MetricClient)

    # Use Cases
    admin_auth_use_case: providers.Factory[AdminAuthUseCase] = providers.Factory(AdminAuthUseCase, uow=unit_of_work)
    admin_token_refresh_use_case: providers.Factory[AdminTokenRefreshUseCase] = providers.Factory(
        AdminTokenRefreshUseCase, uow=unit_of_work
    )
    admin_create_promotion_use_case: providers.Factory[CreatePromotionUseCase] = providers.Factory(
        CreatePromotionUseCase, adapter=fs_adapter, uow=unit_of_work
    )
    admin_delete_promotion_use_case: providers.Factory[DeletePromotionUseCase] = providers.Factory(
        DeletePromotionUseCase, adapter=fs_adapter, uow=unit_of_work
    )
    admin_update_promotion_use_case: providers.Factory[UpdatePromotionUseCase] = providers.Factory(
        UpdatePromotionUseCase, adapter=fs_adapter, uow=unit_of_work
    )
    admin_change_min_fuel_volume_use_case: providers.Factory[ChangeMinFuelVolumeUseCase] = providers.Factory(
        ChangeMinFuelVolumeUseCase, uow=unit_of_work
    )

    auth_init_use_case: providers.Factory[InitUseCase] = providers.Factory(
        InitUseCase,
        uow=unit_of_work,
        settings=settings,
        metric_manager=metric_manager,
        notifications_adapter=notifications_adapter,
        telegram_notification_adapter=telegram_notification_adapter,
    )
    auth_verify_use_case = providers.Factory(VerifyUseCase, uow=unit_of_work)
    auth_logout_use_case = providers.Factory(LogoutUseCase, uow=unit_of_work)
    delete_user_use_case = providers.Factory(DeleteUserUseCase, uow=unit_of_work, metric_manager=metric_manager)
    user_register_use_case = providers.Factory(RegisterUseCase, uow=unit_of_work)
    user_register_agreements_use_case = providers.Factory(
        RegisterAgreementsUseCase,
        uow=unit_of_work,
        metric_manager=metric_manager,
        card_master_adapter=card_master_adapter,
    )
    user_change_user = providers.Factory(ChangeUserUseCase, uow=unit_of_work)
    orders_create_order_request_use_case: providers.Factory[CreateOrderRequestUseCase] = providers.Factory(
        CreateOrderRequestUseCase, adapter=mail_adapter, uow=unit_of_work
    )
    orders_submit_feedback_use_case: providers.Factory[SubmitFeedbackUseCase] = providers.Factory(
        SubmitFeedbackUseCase, adapter=mail_adapter, uow=unit_of_work
    )
    token_refresh_use_case = providers.Factory(RefreshUseCase, uow=unit_of_work)

    # Views
    orders_get_min_fuel_volume_use_case: providers.Factory[GetMinFuelVolumeView] = providers.Factory(
        GetMinFuelVolumeView, uow=unit_of_work
    )
    user_get_user_view = providers.Factory(GetUserView, uow=unit_of_work)
    user_get_fcm_token_view = providers.Factory(GetFCMTokenView, uow=unit_of_work)

    card_get_card_info_view: providers.Factory[GetCardInfoView] = providers.Factory(
        GetCardInfoView, uow=unit_of_work, card_master_adapter=card_master_adapter
    )
    card_get_card_bonuses_view: providers.Factory[GetCardBonusesView] = providers.Factory(
        GetCardBonusesView, uow=unit_of_work, card_master_adapter=card_master_adapter
    )

    orders_get_orders_view: providers.Factory[GetOrdersView] = providers.Factory(GetOrdersView, uow=unit_of_work)

    promotions_get_promotions_view: providers.Factory[GetPromotionsView] = providers.Factory(
        GetPromotionsView, adapter=fs_adapter, uow=unit_of_work
    )
    promotions_get_promotion_view: providers.Factory[GetPromotionView] = providers.Factory(
        GetPromotionView, adapter=fs_adapter, uow=unit_of_work
    )

    stations_get_stations_view: providers.Factory[GetGasStationsView] = providers.Factory(
        GetGasStationsView, uow=unit_of_work
    )
    stations_get_oils_view: providers.Factory[GetOilsView] = providers.Factory(GetOilsView, uow=unit_of_work)
    stations_get_services_view: providers.Factory[GetServicesView] = providers.Factory(
        GetServicesView, uow=unit_of_work
    )

    # CronHandler
    # cron_collector_expired_sessions: providers.Resource[CollectorExpiredSessionsHandler] = providers.Resource(
    #   init_collector_expired_sessions_handler, uow=unit_of_work, settings=settings.provided.auth
    # )
