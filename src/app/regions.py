import logging

from fastapi import APIRouter, Body, HTTPException

from src.app.dependencies import DBDep
from src.schemas.regions import RegionsAdd, RegionsPatch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/regions",
    tags=["Регионы"],
)


@router.get("", name="Получение всех регионов")
async def get_regions(db: DBDep):
    try:
        return await db.regions.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{region_id}", name="Получение одного региона")
async def get_region(region_id: int, db: DBDep):
    try:
        return await db.regions.get_one_ore_none(id=region_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", name="Добавление региона")
async def add_region(
    db: DBDep,
    region: RegionsAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Новый регион",
                "value": {
                    "name": "Московская область",
                },
            }
        }
    ),
):
    try:
        await db.regions.add(region)
        await db.commit()
        return {"status": "OK"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{region_id}", name="Обновление региона (полное)")
async def update_region(region_id: int, region: RegionsAdd, db: DBDep):
    check_status = await db.regions.get_one_ore_none(id=region_id)
    if check_status is None:
        raise HTTPException(status_code=404, detail="Такой регион не найден")
    try:
        await db.regions.edit(region, id=region_id)
        await db.commit()
        return {"status": "OK"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{region_id}", name="Обновление региона (частичное)")
async def partial_update_region(
    region_id: int,
    region: RegionsPatch,
    db: DBDep,
):
    check_status = await db.regions.get_one_ore_none(id=region_id)
    if check_status is None:
        raise HTTPException(status_code=404, detail="Такой регион не найден")
    try:
        await db.regions.edit(
            region,
            exclude_unset=True,
            id=region_id,
        )
        await db.commit()
        return {"status": "OK"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{region_id}", name="Удаление региона")
async def delete_region(region_id: int, db: DBDep):
    check_status = await db.regions.get_one_ore_none(id=region_id)
    if check_status is None:
        raise HTTPException(status_code=404, detail="Такой регион не найден")
    await db.regions.delete_one(id=region_id)
    await db.commit()
    return {"status": "OK", "details": "Регион удален"}
