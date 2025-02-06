from typing import List

from sqlalchemy import select

from repositories.base import BaseRepository
from src.models import ProductsORM
from src.models import ServicesORM
from src.models.products_with_services import (
    ProductsWithServicesORM,
    ProductsWithServicesServices,
)
from src.schemas.products_with_services import ProductsWithServices


class ProductsWithServicesRepository(BaseRepository):
    model = ProductsWithServicesORM
    mapper = ProductsWithServices

    async def add_product_with_service(self, product_id: int, service_ids: List[int]):
        # Получаем цену продукта
        product_query = select(ProductsORM.price).where(ProductsORM.id == product_id)
        product_result = await self.session.execute(product_query)
        product_price = product_result.scalar_one_or_none()

        # Проверяем, что продукт существует
        if product_price is None:
            raise ValueError("Продукт не найден")

        # Получаем цену услуг и суммируем их
        sum_services_prices = 0
        for service_id in service_ids:
            service_query = select(ServicesORM.price).where(
                ServicesORM.id == service_id
            )
            service_result = await self.session.execute(service_query)
            service_price = service_result.scalar_one_or_none()
            if service_price is None:
                raise ValueError(f"Услуга с ID {service_id} не найдена")
            sum_services_prices += service_price

        # Вычисляем общую цену
        total_price = product_price + sum_services_prices
        print(f"Total price: {total_price}")

        # Создаем объект ProductsWithServicesORM
        product_with_service = self.model(
            product_id=product_id,
            service_ids=(
                ",".join(map(str, service_ids)) if service_ids else None
            ),  # Хранение списка service_id в виде строки
            price=total_price,
        )

        # Добавляем объект в сессию и сохраняем
        self.session.add(product_with_service)
        await self.session.commit()
        await self.session.refresh(product_with_service)

        # Добавляем связи многие-ко-многим
        if service_ids:
            for service_id in service_ids:
                service_link = ProductsWithServicesServices(
                    product_with_service_id=product_with_service.id,
                    service_id=service_id,
                )
                self.session.add(service_link)
        await self.session.commit()

        # Возвращаем результат в нужном формате
        return {
            "product_id": product_with_service.product_id,
            "service_ids": (
                [int(sid) for sid in product_with_service.service_ids.split(",")]
                if product_with_service.service_ids
                else None
            ),
            "price": product_with_service.price,
        }
