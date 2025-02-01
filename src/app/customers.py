import logging

from fastapi import APIRouter, Body, HTTPException

from src.app.dependencies import DBDep
from src.schemas.customers import CustomersAdd, CustomersPatch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/customers",
    tags=["Клиенты"],
)


@router.get("", name="Получение всех клиентов")
async def get_customers(db: DBDep):
    try:
        return await db.customers.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{customer_id}", name="Получение одного клиента")
async def get_customer(customer_id: int, db: DBDep):
    try:
        return await db.customers.get_one_ore_none(id=customer_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", name="Добавление клиента")
async def add_customer(
    db: DBDep,
    customer: CustomersAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Новый клиент",
                "value": {
                    "first_name": "Иван",
                    "last_name": "Иванов",
                    "email": "ivan.ivanov@example.com",
                    "phone": "+7 911 8888888",
                    "address": "Москва, ул. Ленина, д. 1",
                    "birth_date": "1990-01-01",
                },
            }
        }
    ),
):
    try:
        logger.info(f"Adding new customer: {customer}")
        await db.customers.add(customer)
        await db.commit()
        return {"status": "OK"}
    except Exception as e:
        logger.error(f"Error adding customer: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{customer_id}", name="Обновление клиента (полное)")
async def update_customer(customer_id: int, customer: CustomersAdd, db: DBDep):
    check_status = await db.customers.get_one_ore_none(id=customer_id)
    if check_status is None:
        raise HTTPException(status_code=404, detail="Такой клиент не найден")
    try:
        await db.customers.edit(customer, id=customer_id)
        await db.commit()
        return {"status": "OK"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{customer_id}", name="Обновление клиента (частичное)")
async def partial_update_customer(
    customer_id: int,
    customer: CustomersPatch,
    db: DBDep,
):
    check_status = await db.customers.get_one_ore_none(id=customer_id)
    if check_status is None:
        raise HTTPException(status_code=404, detail="Такой клиент не найден")
    try:
        await db.customers.edit(
            customer,
            exclude_unset=True,
            id=customer_id,
        )
        await db.commit()
        return {"status": "OK"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{customer_id}", name="Удаление клиента")
async def delete_customer(customer_id: int, db: DBDep):
    check_status = await db.customers.get_one_ore_none(id=customer_id)
    if check_status is None:
        raise HTTPException(status_code=404, detail="Такой клиент не найден")
    await db.customers.delete_one(id=customer_id)
    await db.commit()
    return {"status": "OK", "details": "Клиент удален"}
