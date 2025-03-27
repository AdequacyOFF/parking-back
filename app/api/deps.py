from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from app.api.errors.api_error import AccessDeniedApiError
from app.dependencies.web_app import WebAppContainer
from app.domain.admin import Admin
from app.repositories.exception import RepositoryNotFoundException
from app.repositories.uow import UnitOfWork
from app.utils.auth.jwt import AuthJWT
from app.utils.auth.schemas import AccessTokenData


@inject
async def auth_admin(
    token_data: AccessTokenData = Depends(AuthJWT.access_status_required()),
    uow: UnitOfWork = Depends(Provide[WebAppContainer.unit_of_work]),
) -> Admin:
    async with uow.begin():
        try:
            admin = await uow.admin_repository.get(admin_id=token_data.user.id)
        except RepositoryNotFoundException:
            raise AccessDeniedApiError
        return admin
