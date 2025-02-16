import logging
from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel
from sqlalchemy import insert, select

from src.models import (
    OrdersORM,
    ProductsORM,
    ServicesORM,
)
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import OrdersMapper

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)


class OrdersRepository(BaseRepository):
    model = OrdersORM
    mapper = OrdersMapper

    async def add_order(
        self,
        data: BaseModel,
        product_ids: Optional[List[int]] = None,
        service_ids: Optional[List[int]] = None,
    ):
        """
        Добавляет заказ и привязывает к нему продукты и сервисы.
        :param data: Данные для создания заказа (схема Pydantic).
        :param product_ids: Список ID продуктов (опционально).
        :param service_ids: Список ID сервисов (опционально).
        :return: Созданный заказ.
        """
        try:
            # Добавляем заказ в базу данных
            add_data_stmt = (
                insert(self.model).values(**data.model_dump()).returning(self.model)
            )
            logger.debug(f"Executing statement: {add_data_stmt}")

            result = await self.session.execute(add_data_stmt)
            order = result.scalars().one()
            logger.debug(f"Order created: {order}")

            # Если указаны product_ids и service_ids, привязываем их к заказу
            if product_ids or service_ids:
                total_price = Decimal("0.0")
                logger.debug(f"Initial total_price: {total_price}")

                # Привязываем продукты
                if product_ids:
                    products_query = select(ProductsORM).where(
                        ProductsORM.id.in_(product_ids)
                    )
                    logger.debug(f"Fetching products with IDs: {product_ids}")

                    products_result = await self.session.execute(products_query)
                    products = products_result.scalars().all()
                    logger.debug(f"Create product objects: {products}")
                    print(f"products: {products}")

                    if len(products) != len(product_ids):
                        raise ValueError("Один или несколько продуктов не найдены")
                    print("Здесь ошибка!")
                    # order.products.extend(products)
                    # Подготовка данных для вставки
                    order_products_values = [
                        {"order_id": order.id, "product_id": product.id}
                        for product in products
                    ]
                    insert_stmt = insert(self.model.order_products).values(
                        order_products_values
                    )
                    await self.session.execute(insert_stmt)

                    total_price += sum(product.price for product in products)
                    logger.debug(f"Products added. Updated total_price: {total_price}")
                    # total_price += sum(product.price for product in products)
                    # print(f"total_price: {total_price}")
                    # logger.debug(f"Products added. Updated total_price: {total_price}")

                # Привязываем сервисы
                if service_ids:
                    services_query = select(ServicesORM).where(
                        ServicesORM.id.in_(service_ids)
                    )
                    logger.debug(f"Fetching services with IDs: {service_ids}")

                    services_result = await self.session.execute(services_query)
                    services = services_result.scalars().all()

                    if len(services) != len(service_ids):
                        raise ValueError("Один или несколько сервисов не найдены")

                        # Подготовка данных для вставки
                    order_services_values = [
                        {"order_id": order.id, "service_id": service.id}
                        for service in services
                    ]
                    insert_stmt = insert(self.model.order_services).values(
                        order_services_values
                    )
                    await self.session.execute(insert_stmt)
                    total_price += sum(service.price for service in services)
                    logger.debug(f"Services added. Updated total_price: {total_price}")

                # Обновляем общую стоимость заказа
                order.total_price = total_price
                logger.debug(f"Final total_price set to: {total_price}")

                # Сохраняем изменения
                self.session.add(order)
                await self.session.commit()
                await self.session.refresh(order)
                logger.debug("Changes committed and order refreshed.")

            # Возвращаем созданный заказ
            logger.debug("Order added successfully.")
            return self.mapper.map_to_domain_entity(order)

        except Exception as e:
            logger.error(f"Error occurred: {e}")
            raise
