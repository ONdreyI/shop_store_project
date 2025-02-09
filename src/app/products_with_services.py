import logging
from fastapi import APIRouter, Body, HTTPException
from src.app.dependencies import DBDep
from src.schemas.products_with_services import (
    ProductsWithServicesAdd,
    ProductsWithServicesPatch,
)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создание роутера
router = APIRouter(
    prefix="/products_with_services",
    tags=["Продукты с сервисами"],
)


@router.get("", name="Получение всех продуктов с сервисами")
async def get_all_products_with_services(
    db: DBDep,
    page: int = 1,
    per_page: int = 5,
):
    try:
        products_with_services = (
            await db.products_with_services.get_all_with_pagination(
                page=page,
                per_page=per_page,
            )
        )
        return products_with_services
    except Exception as e:
        logger.error(f"Ошибка при получении всех продуктов с сервисами: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", name="Добавление продукта с сервисом")
async def add_product_with_service(
    db: DBDep,
    product_with_service: ProductsWithServicesAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Продукт с сервисом",
                "value": {
                    "product_id": 132,
                    "service_ids": [16, 17],
                },
            }
        }
    ),
):
    try:
        await db.products_with_services.add_product_with_service(
            product_with_service.product_id,
            product_with_service.service_ids,
        )
        return {"status": "OK"}
    except Exception as e:
        logger.error(f"Ошибка при добавлении продукта с сервисом: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/products", name="Проверка статуса")
async def get_product_status(
    db: DBDep,
    pws_id: int,
    product_id: int,
):
    try:
        raise db.products_with_services.new_method(
            pws_id=pws_id,
            product_id=product_id,
        )
    except Exception as e:
        logger.error(f"Ошибка при получении статуса продукта с сервисом: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{id}", name="Удаление или добавление услуг")
async def update_pws(
    db: DBDep,
    pws_id: int,
    pws_data: ProductsWithServicesPatch,
):
    check_status = await db.products_with_services.get_one_ore_none(
        id=pws_id,
    )
    if check_status is None:
        logger.error(f"Продукт с сервисом не найден, id: {pws_id}")
        raise HTTPException(
            status_code=404, detail="Такой продукт с сервисом не найден"
        )
    try:
        await db.products_with_services.edit_pws(
            data=pws_data,
            id=pws_id,
        )
        return {"status": "OK", "data": pws_data}
    except Exception as e:
        logger.error(
            f"Ошибка при удалении или добавлении услуг продукта с сервисом: {e}"
        )
        raise HTTPException(status_code=500, detail=str(e))


#
#
# @router.patch("/{id}", name="Обновление продукта с сервисом (частичное)")
# async def partial_update_product_with_service(
#     pws_id: int,
#     product_with_service: ProductsWithServicesPatch,
#     db: DBDep,
# ):
#     try:
#         await db.products_with_services.edit_pws(
#             data=product_with_service,
#             exclude_unset=True,
#             id=pws_id,
#         )
#         await db.commit()
#         return {"status": "OK"}
#     except Exception as e:
#         logger.error(f"Ошибка при частичном обновлении продукта с сервисом: {e}")
#         raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{id}", name="Удаление продукта с сервисом")
async def delete_product_with_service(
    id: int,
    product_id: int,
    db: DBDep,
):
    check_status = await db.products_with_services.get_one_ore_none(
        id=id,
        product_id=product_id,
    )
    if check_status is None:
        logger.error(f"Продукт с сервисом не найден, id: {id}")
        raise HTTPException(
            status_code=404, detail="Такой продукт с сервисом не найден"
        )
    await db.products_with_services.delete_one(id=id)
    await db.commit()
    logger.info(f"Продукт с сервисом удален, id: {id}")
    return {"status": "OK", "details": "Продукт с сервисом удален"}
