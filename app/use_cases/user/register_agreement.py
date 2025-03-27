from uuid import UUID

from app.adapters.card_master.adapter import CardMasterAdapter
from app.adapters.card_master.exception import CardExceedAdapterError
from app.api.errors.api_error import AgreementsNotAcceptedApiError, NoAvailableCardApiError, UserNotFoundApiError
from app.api.user.schemas import RegisterAgreementsCMD, RegisterAgreementsResponse
from app.domain.exception import AgreementsNotAcceptedException
from app.domain.user import Card
from app.dto.card import CardType, CreateCardCMD
from app.dto.user import AcceptAgreementsCMD
from app.infrastructure.metrics import MetricClient, MetricsType
from app.repositories.exception import RepositoryNotFoundException
from app.repositories.uow import UnitOfWork


class RegisterAgreementsUseCase:
    def __init__(self, uow: UnitOfWork, metric_manager: MetricClient, card_master_adapter: CardMasterAdapter):
        self._uow = uow
        self._card_master_adapter = card_master_adapter
        self._metric_manager = metric_manager

    async def __call__(self, cmd: RegisterAgreementsCMD, user_id: UUID) -> RegisterAgreementsResponse:
        async with self._uow.begin():
            try:
                user = await self._uow.user_repository.get(user_id)
            except RepositoryNotFoundException as e:
                raise UserNotFoundApiError from e

            try:
                user.accept_agreements(
                    cmd=AcceptAgreementsCMD(
                        user_agreement=cmd.user_agreement,
                        privacy_policy=cmd.privacy_policy,
                        company_rules=cmd.company_rules,
                    )
                )
            except AgreementsNotAcceptedException as e:
                raise AgreementsNotAcceptedApiError from e

            if user.card is None:
                try:
                    card_result = await self._card_master_adapter.fetch_card()
                except CardExceedAdapterError:
                    raise NoAvailableCardApiError

                card = Card.create(cmd=CreateCardCMD(qr=card_result.card_id, type=CardType.BRONZE))
                user.create_bonus_card(card)

            await self._uow.user_repository.save(user)

            self._metric_manager.register_metric(MetricsType.REGISTERED_USER)

        return RegisterAgreementsResponse()
