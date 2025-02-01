import logging

from fastapi import APIRouter, Body, HTTPException

from src.app.dependencies import DBDep
from src.schemas.managers import ManagersAdd, ManagersPatch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/managers",
    tags=["Менеджеры"],
)


@router.get("", name="Получение всех менеджеров")
async def get_managers(db: DBDep):
    try:
        return await db.managers.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{manager_id}", name="Получение одного менеджера")
async def get_manager(manager_id: int, db: DBDep):
    try:
        return await db.managers.get_one_ore_none(id=manager_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", name="Добавление менеджера")
async def add_manager(
    db: DBDep,
    manager: ManagersAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Новый менеджер",
                "value": {
                    "first_name": "Алексей",
                    "last_name": "Петров",
                    "department": "Отдел продаж",
                },
            }
        }
    ),
):
    try:
        await db.managers.add(manager)
        await db.commit()
        return {"status": "OK"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{manager_id}", name="Обновление менеджера (полное)")
async def update_manager(manager_id: int, manager: ManagersAdd, db: DBDep):
    check_status = await db.managers.get_one_ore_none(id=manager_id)
    if check_status is None:
        raise HTTPException(status_code=404, detail="Такой менеджер не найден")
    try:
        await db.managers.edit(manager, id=manager_id)
        await db.commit()
        return {"status": "OK"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{manager_id}", name="Обновление менеджера (частичное)")
async def partial_update_manager(
    manager_id: int,
    manager: ManagersPatch,
    db: DBDep,
):
    check_status = await db.managers.get_one_ore_none(id=manager_id)
    if check_status is None:
        raise HTTPException(status_code=404, detail="Такой менеджер не найден")
    try:
        await db.managers.edit(
            manager,
            exclude_unset=True,
            id=manager_id,
        )
        await db.commit()
        return {"status": "OK"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{manager_id}", name="Удаление менеджера")
async def delete_manager(manager_id: int, db: DBDep):
    check_status = await db.managers.get_one_ore_none(id=manager_id)
    if check_status is None:
        raise HTTPException(status_code=404, detail="Такой менеджер не найден")
    await db.managers.delete_one(id=manager_id)
    await db.commit()
    return {"status": "OK", "details": "Менеджер удален"}
