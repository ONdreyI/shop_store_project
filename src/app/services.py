import logging

from fastapi import APIRouter, Body, HTTPException

from src.database import async_session_maker
from src.models import ServicesORM
from src.repositories.services import ServicesRepository
from src.schemas.services import ServicesAdd, ServicesPatch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/services",
    tags=["Сервисы"],
)


@router.get("", name="Получение всех услуг")
async def get_services():
    async with async_session_maker() as session:
        try:
            return await ServicesRepository(session).get_all()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@router.get("/{service_id}", name="Получение одной услуги")
async def get_service(service_id: int):
    async with async_session_maker() as session:
        try:
            return await ServicesRepository(session).get_one_ore_none(id=service_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@router.post("", name="Добавление услуги")
async def add_service(
    service: ServicesAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Доставка",
                "value": {
                    "name": "Доставка",
                    "price": 1299.99,
                },
            }
        }
    )
):
    async with async_session_maker() as session:
        try:
            await ServicesRepository(session).add(service)
            await session.commit()
            return {"status": "OK"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@router.put("/{service_id}", name="Обновление услуги (полное)")
async def update_service(service_id: int, service: ServicesAdd):
    async with async_session_maker() as session:
        db_service = await session.get(ServicesORM, service_id)
        if db_service is None:
            raise HTTPException(status_code=404, detail="Такой сервис не найден")
        try:
            await ServicesRepository(session).edit(service, id=service_id)
            return {"status": "OK"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{service_id}", name="Обновление услуги (частичное)")
async def partial_update_service(service_id: int, service: ServicesPatch):
    async with async_session_maker() as session:
        db_service = await session.get(ServicesORM, service_id)
        if db_service is None:
            raise HTTPException(status_code=404, detail="Такой сервис не найден")
        try:
            await ServicesRepository(session).edit(
                service,
                exclude_unset=True,
                id=service_id,
            )
            return {"status": "OK"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{service_id}", name="Удаление услуги")
async def delete_service(service_id: int):
    async with async_session_maker() as session:
        db_service = await session.get(ServicesORM, service_id)
        if db_service is None:
            raise HTTPException(status_code=404, detail="Такой сервис не найден")
        await ServicesRepository(session).delete_one(id=service_id)
    return {"status": "OK", "details": "Сервис удален"}
