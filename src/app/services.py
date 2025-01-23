from fastapi import APIRouter


router = APIRouter(
    prefix="/services",
    tags=["Сервисы"],
)


@router.get("")
async def get_services():
    pass
