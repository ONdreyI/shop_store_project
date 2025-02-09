import logging

from fastapi import APIRouter, Body, HTTPException

from src.app.dependencies import DBDep
from src.schemas.services import ServicesAdd, ServicesPatch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/services",
    tags=["Сервисы"],
)


@router.get("", name="Получение всех услуг")
async def get_services(db: DBDep):
    try:
        return await db.services.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{service_id}", name="Получение одной услуги")
async def get_service(service_id: int, db: DBDep):
    try:
        return await db.services.get_one_ore_none(id=service_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", name="Добавление услуги")
async def add_service(
    db: DBDep,
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
    ),
):
    try:
        await db.services.add(service)
        await db.commit()
        return {"status": "OK"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{service_id}", name="Обновление услуги (полное)")
async def update_service(service_id: int, service: ServicesAdd, db: DBDep):
    check_status = await db.services.get_one_ore_none(id=service_id)
    if check_status is None:
        raise HTTPException(status_code=404, detail="Такой сервис не найден")
    try:
        await db.services.edit(service, id=service_id)
        return {"status": "OK"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{service_id}", name="Обновление услуги (частичное)")
async def partial_update_service(
    service_id: int,
    service: ServicesPatch,
    db: DBDep,
):
    check_status = await db.services.get_one_ore_none(id=service_id)
    if check_status is None:
        raise HTTPException(status_code=404, detail="Такой сервис не найден")
    try:
        await db.services.edit(
            service,
            exclude_unset=True,
            id=service_id,
        )
        return {"status": "OK"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{service_id}", name="Удаление услуги")
async def delete_service(service_id: int, db: DBDep):
    check_status = await db.services.get_one_ore_none(id=service_id)
    if check_status is None:
        raise HTTPException(status_code=404, detail="Такой сервис не найден")
    await db.services.delete_one(id=service_id)
    await db.commit()
    return {"status": "OK", "details": "Сервис удален"}
