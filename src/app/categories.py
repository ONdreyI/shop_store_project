import logging

from fastapi import APIRouter, Body, HTTPException

from src.app.dependencies import DBDep
from src.schemas.categories import CategoriesAdd, CategoriesPatch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/categories",
    tags=["Категории"],
)


@router.get("", name="Получение всех категорий")
async def get_categories(db: DBDep):
    try:
        return await db.categories.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{category_id}", name="Получение одной категории")
async def get_category(category_id: int, db: DBDep):
    try:
        return await db.categories.get_one_ore_none(id=category_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", name="Добавление категории")
async def add_category(
    db: DBDep,
    category: CategoriesAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Электроника",
                "value": {
                    "name": "Электроника",
                },
            }
        }
    ),
):
    try:
        await db.categories.add(category)
        await db.commit()
        return {"status": "OK"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{category_id}", name="Обновление категории (полное)")
async def update_category(category_id: int, category: CategoriesAdd, db: DBDep):
    check_status = await db.categories.get_one_ore_none(id=category_id)
    if check_status is None:
        raise HTTPException(status_code=404, detail="Такая категория не найдена")
    try:
        await db.categories.edit(category, id=category_id)
        return {"status": "OK"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{category_id}", name="Обновление категории (частичное)")
async def partial_update_category(
    category_id: int,
    category: CategoriesPatch,
    db: DBDep,
):
    check_status = await db.categories.get_one_ore_none(id=category_id)
    if check_status is None:
        raise HTTPException(status_code=404, detail="Такая категория не найдена")
    try:
        await db.categories.edit(
            category,
            exclude_unset=True,
            id=category_id,
        )
        return {"status": "OK"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{category_id}", name="Удаление категории")
async def delete_category(category_id: int, db: DBDep):
    check_status = await db.categories.get_one_ore_none(id=category_id)
    if check_status is None:
        raise HTTPException(status_code=404, detail="Такая категория не найдена")
    await db.categories.delete_one(id=category_id)
    await db.commit()
    return {"status": "OK", "details": "Категория удалена"}
