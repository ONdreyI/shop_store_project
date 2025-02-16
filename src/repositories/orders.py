import logging
from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel
from sqlalchemy import insert, select, delete
from sqlalchemy.orm import selectinload

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

                    if len(products) != len(product_ids):
                        raise ValueError("Один или несколько продуктов не найдены")
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

    async def edit_order(
        self,
        order_id: int,
        add_product_ids: Optional[List[int]] = None,
        remove_product_ids: Optional[List[int]] = None,
        add_service_ids: Optional[List[int]] = None,
        remove_service_ids: Optional[List[int]] = None,
    ):
        """
        Редактирует заказ, добавляя или удаляя продукты и сервисы.
        :param order_id: ID заказа для редактирования.
        :param add_product_ids: Список ID продуктов для добавления (опционально).
        :param remove_product_ids: Список ID продуктов для удаления (опционально).
        :param add_service_ids: Список ID сервисов для добавления (опционально).
        :param remove_service_ids: Список ID сервисов для удаления (опционально).
        :return: Обновленный заказ.
        """
        try:
            # Получаем текущий заказ
            order = await self.session.get(self.model, order_id)
            if not order:
                raise ValueError("Заказ не найден")

            total_price_change = Decimal("0.0")

            # Добавляем новые продукты
            if add_product_ids:
                products_query = select(ProductsORM).where(
                    ProductsORM.id.in_(add_product_ids)
                )
                products_result = await self.session.execute(products_query)
                products = products_result.scalars().all()

                if len(products) != len(add_product_ids):
                    raise ValueError("Один или несколько продуктов не найдены")

                order_products_values = [
                    {"order_id": order.id, "product_id": product.id}
                    for product in products
                ]
                insert_stmt = insert(self.model.order_products).values(
                    order_products_values
                )
                await self.session.execute(insert_stmt)

                total_price_change += sum(product.price for product in products)

            # Удаляем продукты
            if remove_product_ids:
                delete_stmt = delete(self.model.order_products).where(
                    (self.model.order_products.c.order_id == order.id)
                    & (self.model.order_products.c.product_id.in_(remove_product_ids))
                )
                await self.session.execute(delete_stmt)

                # Получаем удаленные продукты для обновления total_price
                removed_products_query = select(ProductsORM).where(
                    ProductsORM.id.in_(remove_product_ids)
                )
                removed_products_result = await self.session.execute(
                    removed_products_query
                )
                removed_products = removed_products_result.scalars().all()

                total_price_change -= sum(product.price for product in removed_products)

            # Добавляем новые сервисы
            if add_service_ids:
                services_query = select(ServicesORM).where(
                    ServicesORM.id.in_(add_service_ids)
                )
                services_result = await self.session.execute(services_query)
                services = services_result.scalars().all()

                if len(services) != len(add_service_ids):
                    raise ValueError("Один или несколько сервисов не найдены")

                order_services_values = [
                    {"order_id": order.id, "service_id": service.id}
                    for service in services
                ]
                insert_stmt = insert(self.model.order_services).values(
                    order_services_values
                )
                await self.session.execute(insert_stmt)

                total_price_change += sum(service.price for service in services)

            # Удаляем сервисы
            if remove_service_ids:
                delete_stmt = delete(self.model.order_services).where(
                    (self.model.order_services.c.order_id == order.id)
                    & (self.model.order_services.c.service_id.in_(remove_service_ids))
                )
                await self.session.execute(delete_stmt)

                # Получаем удаленные сервисы для обновления total_price
                removed_services_query = select(ServicesORM).where(
                    ServicesORM.id.in_(remove_service_ids)
                )
                removed_services_result = await self.session.execute(
                    removed_services_query
                )
                removed_services = removed_services_result.scalars().all()

                total_price_change -= sum(service.price for service in removed_services)

            # Обновляем общую стоимость заказа
            order.total_price += total_price_change
            await self.session.commit()
            await self.session.refresh(order)

            # Возвращаем обновленный заказ
            return self.mapper.map_to_domain_entity(order)

        except Exception as e:
            logger.error(f"Error occurred: {e}")
            raise

    async def get_one_or_none_order(self, order_id: int):
        """
        Получает заказ по его ID вместе со списком продуктов и сервисов.
        :param order_id: ID заказа для получения.
        :return: Заказ с продуктами и сервисами или None, если заказ не найден.
        """
        try:
            # Получаем заказ с предварительной загрузкой продуктов, сервисов и связанных сущностей
            order_query = (
                select(OrdersORM)
                .options(
                    selectinload(OrdersORM.products),
                    selectinload(OrdersORM.services),
                    selectinload(OrdersORM.customer),
                    selectinload(OrdersORM.manager),
                    selectinload(OrdersORM.region),
                )
                .filter_by(id=order_id)
            )
            result = await self.session.execute(order_query)
            order = result.scalars().one_or_none()

            if order is None:
                return None

            # Преобразуем продукты и сервисы в список названий
            product_names = [product.name for product in order.products]
            service_names = [service.name for service in order.services]

            # Формируем данные заказа
            order_data = {
                "id": order.id,
                "order_date": order.order_date,
                "customer": f"{order.customer.last_name} {order.customer.first_name}",
                "manager": f"{order.manager.last_name} {order.manager.first_name}",
                "region": order.region.name,
                "total_price": order.total_price,
                "products": product_names,
                "services": service_names,
            }

            return order_data

        except Exception as e:
            logger.error(f"Ошибка при получении заказа: {e}")
            raise
