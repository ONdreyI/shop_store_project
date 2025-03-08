import asyncio
from time import sleep

from src.database import async_session_maker_null_pool
from src.tasks.celery_app import celery_instance
from src.logging_config import logger
from src.utils.db_manager import DBManager


@celery_instance.task
def test_task():
    sleep(5)
    print("Я МОЛОДЕЦ!!!")


async def create_refresh_monthly_order_summary_redis():
    logger.info("Я ЗАПУСКАЮСЬ!!!")
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        monthly_order_summary = (
            await db.monthly_order_summary.refresh_monthly_order_summary()
        )
        logger.info(f"Обновленная статистика заказов: {monthly_order_summary}")


@celery_instance.task()
def create_refresh_monthly_order_redis():
    asyncio.run(create_refresh_monthly_order_summary_redis())
