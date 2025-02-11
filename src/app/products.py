import logging

from fastapi import APIRouter, Body, HTTPException

from src.app.dependencies import DBDep
from src.schemas.products import ProductsAdd, ProductsPatch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/products",
    tags=["Продукты"],
)


@router.get("", name="Получение всех продуктов")
async def get_products(
    db: DBDep,
    page: int = 1,
    per_page: int = 10,
):
    try:
        return await db.products.get_all_with_pagination(
            page=page,
            per_page=per_page,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{product_id}", name="Получение одного продукта")
async def get_product(product_id: int, db: DBDep):
    check_status = await db.products.get_one_ore_none(id=product_id)
    if check_status is None:
        raise HTTPException(status_code=404, detail="Такой продукт не найден")
    try:
        return await db.products.get_products_with_categories(product_id=product_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/{product_id}/category_id", name="Поиск всех продуктов по выбранной категории"
)
async def get_products_by_category_id(
    db: DBDep,
    category_id: int,
    page: int = 1,
    per_page: int = 5,
):
    check_status = await db.categories.get_one_ore_none(id=category_id)
    if check_status is None:
        raise HTTPException(status_code=404, detail="Такая категория не найдена")
    try:
        return await db.products.get_products_by_category(
            category_id=category_id,
            page=page,
            per_page=per_page,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", name="Добавление продукта")
async def add_product(
    db: DBDep,
    product: ProductsAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Новый продукт",
                "value": {
                    "name": "Новый продукт",
                    "category_id": 1,
                    "price": 999.99,
                },
            }
        }
    ),
):
    try:
        await db.products.add(product)
        await db.commit()
        return {"status": "OK"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{product_id}", name="Обновление продукта (полное)")
async def update_product(product_id: int, product: ProductsAdd, db: DBDep):
    check_status = await db.products.get_one_ore_none(id=product_id)
    if check_status is None:
        raise HTTPException(status_code=404, detail="Такой продукт не найден")
    try:
        await db.products.edit(product, id=product_id)
        return {"status": "OK"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{product_id}", name="Обновление продукта (частичное)")
async def partial_update_product(
    product_id: int,
    product: ProductsPatch,
    db: DBDep,
):
    check_status = await db.products.get_one_ore_none(id=product_id)
    if check_status is None:
        raise HTTPException(status_code=404, detail="Такой продукт не найден")
    try:
        await db.products.edit(
            product,
            exclude_unset=True,
            id=product_id,
        )
        return {"status": "OK"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{product_id}", name="Удаление продукта")
async def delete_product(product_id: int, db: DBDep):
    check_status = await db.products.get_one_ore_none(id=product_id)
    if check_status is None:
        raise HTTPException(status_code=404, detail="Такой продукт не найден")
    await db.products.delete_one(id=product_id)
    await db.commit()
    return {"status": "OK", "details": "Продукт удален"}
