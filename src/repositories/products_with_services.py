from sqlalchemy import select

from src.models import ServicesORM
from src.models import ProductsORM
from repositories.base import BaseRepository
from src.models import ProductsWithServicesORM
from src.schemas.products_with_services import (
    ProductsWithServicesAdd,
    ProductsWithServices,
)


class ProductsWithServicesRepository(BaseRepository):
    model = ProductsWithServicesORM
    mapper = ProductsWithServices

    async def add_product_with_service(self, product_id: int, service_id: int):
        # Получаем цену продукта
        product_query = select(ProductsORM.price).where(ProductsORM.id == product_id)
        product_result = await self.session.execute(product_query)
        product_price = product_result.scalar_one_or_none()

        # Получаем цену сервиса
        if service_id:
            service_query = select(ServicesORM.price).where(
                ServicesORM.id == service_id
            )
            service_result = await self.session.execute(service_query)
            service_price = service_result.scalar_one_or_none()
        else:
            service_price = 0

        # Проверяем, что product существует
        if product_price is None:
            raise ValueError("Продукт не найден")

        # Вычисляем общую цену
        total_price = product_price + (service_price or 0)
        print(f"Total price: {total_price}")

        # Создаем объект ProductsWithServicesORM
        product_with_service = self.model(
            product_id=product_id,
            service_id=service_id,
            price=total_price,
        )

        # Добавляем объект в сессию и сохраняем
        self.session.add(product_with_service)
        await self.session.commit()
        await self.session.refresh(product_with_service)

        # Возвращаем результат в нужном формате
        return {
            "product_id": product_with_service.product_id,
            "service_id": product_with_service.service_id,
            "price": product_with_service.price,
        }
