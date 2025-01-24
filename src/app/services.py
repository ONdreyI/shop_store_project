from fastapi import APIRouter, Body, HTTPException
import logging
from sqlalchemy import insert, select
from src.database import async_session_maker
from src.models import ServicesORM
from src.schemas.services import ServicesAdd, Services, ServicesPatch


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/services",
    tags=["Сервисы"],
)


@router.get("")
async def get_services():
    async with async_session_maker() as session:
        try:
            result = await session.execute(select(ServicesORM))
            services = result.scalars().all()
            return [Services.from_orm(serv) for serv in services]
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
        add_service_stmt = insert(ServicesORM).values(**service.model_dump())
        await session.execute(add_service_stmt)
        await session.commit()

    return {"status": "OK"}


@router.put("/{id}", name="Обновление услуги (полное)")
async def update_service(id: int, service: ServicesAdd):
    async with async_session_maker() as session:
        db_service = await session.get(ServicesORM, id)
        if db_service is None:
            raise HTTPException(status_code=404, detail="Такой сервис не найден")
        for key, value in service.dict(exclude_unset=True).items():
            setattr(db_service, key, value)
        await session.commit()
        await session.refresh(db_service)
        return {"status": "ok", "Данные обновились": db_service}


@router.patch("/{id}", name="Обновление услуги (частичное)")
async def partial_update_service(id: int, service: ServicesPatch):
    async with async_session_maker() as session:
        async with session.begin():
            try:
                db_service = await session.get(ServicesORM, id)
                if db_service is None:
                    raise HTTPException(
                        status_code=404, detail="Такой сервис не найден"
                    )

                update_data = service.dict(exclude_unset=True)
                for key, value in update_data.items():
                    setattr(db_service, key, value)

                await session.commit()
                await session.refresh(db_service)

                return {"status": "ok", "Данные обновились": db_service}
            except Exception as e:
                logger.error(f"Ошибка при обновлении услуги: {str(e)}")
                raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.delete("/{id}", name="Удаление услуги")
async def delete_service(id: int):
    async with async_session_maker() as session:
        db_service = await session.get(ServicesORM, id)
        if db_service is None:
            raise HTTPException(status_code=404, detail="Такой сервис не найден")
        await session.delete(db_service)
        await session.commit()
        return {"status": "ok", "details": "Сервис удален"}
