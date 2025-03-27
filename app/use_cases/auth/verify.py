from app.api.auth.schemas import VerifyCMD, VerifyResponse
from app.api.errors.api_error import InvalidOTPApiError, OTPExpiredApiError, UserNotFoundApiError
from app.domain.exception import InvalidOTPException, OTPExpiredException
from app.dto.user import DeviceInfo, VerifyOTPUserDTO
from app.repositories.exception import RepositoryNotFoundException
from app.repositories.uow import UnitOfWork
from app.utils.auth.jwt import AuthJWT
from app.utils.auth.schemas import UserData


class VerifyUseCase:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def __call__(self, cmd: VerifyCMD) -> VerifyResponse:
        async with self._uow.begin():
            try:
                user = await self._uow.user_repository.get_by_phone_number(cmd.phone_number)
            except RepositoryNotFoundException as e:
                raise UserNotFoundApiError from e

            refresh_data = AuthJWT.create_refresh_token(user_data=UserData(id=user.id, status=user.status))

            try:
                user.verify_otp(
                    cmd=VerifyOTPUserDTO(
                        otp=cmd.otp,
                        session_id=refresh_data.jti,
                        token=refresh_data.token,
                        device=DeviceInfo(**cmd.device.dict()),
                    )
                )
            except InvalidOTPException as e:
                await self._uow.user_repository.save(user)
                await self._uow.commit()
                raise InvalidOTPApiError from e
            except OTPExpiredException as e:
                raise OTPExpiredApiError from e

            await self._uow.user_repository.save(user)

            access_data = AuthJWT.create_access_token(
                user_data=UserData(id=user.id, status=user.status), jti=refresh_data.jti
            )
            return VerifyResponse(access=access_data.token, refresh=refresh_data.token)
