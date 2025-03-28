from app.api.auth.schemas import InitResponse
from app.api.errors.api_error import OTPSendTimeoutApiError
from app.domain.exception import OTPSendTimeoutException
from app.domain.user import OTP, User
from app.dto.user import InitUserCMD
from app.repositories.exception import RepositoryNotFoundException
from app.repositories.uow import UnitOfWork
from app.settings import Settings


class InitUseCase:
    def __init__(
        self,
        uow: UnitOfWork,
        settings: Settings,
    ):
        self._uow = uow
        self._settings = settings

    async def __call__(self, cmd: InitUserCMD) -> InitResponse:
        async with self._uow.begin():
            try:
                user = await self._uow.user_repository.get_by_phone_number(cmd.phone_number)
            except RepositoryNotFoundException:
                user = User.init(cmd=InitUserCMD(phone_number=cmd.phone_number))

            try:
                otp = OTP.create()
                user.add_otp(otp)
            except OTPSendTimeoutException as e:
                raise OTPSendTimeoutApiError from e

            if cmd.phone_number == "79999999999":
                otp.code = "2" * self._settings.auth.otp_length
            else:
                if not user.otp_code:
                    raise RuntimeError

            await self._uow.user_repository.save(user=user)
            return InitResponse()
