from fastapi import APIRouter

router = APIRouter(prefix="/srv")


@router.get("/health", response_model=bool, include_in_schema=False)
async def ping() -> bool:
    return True
