from typing import List

from sqlalchemy import select, delete, insert

from src.models import ProductsORM
from src.models import ServicesORM
from src.models.products_with_services import (
    ProductsWithServicesORM,
    ProductsWithServicesServices,
)
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import ProductsWithServicesMapper
from src.schemas.products_with_services import (
    ProductsWithServices,
    ProductsWithServicesAdd,
)


class ProductsWithServicesRepository(BaseRepository):
    model = ProductsWithServicesORM
    mapper = ProductsWithServicesMapper

    async def add_product_with_service(
            self,
            product_id: int,
            service_ids: List[int],
    ):
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
            service_ids=service_ids,  # Хранение списка service_id в виде массива
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

        # Возвращаем результат в виде схемы Pydantic
        return ProductsWithServices.model_validate(product_with_service)

    async def edit_pws(
            self,
            data: ProductsWithServicesAdd,
            exclude_unset: bool = True,
            **filter_by,
    ):
        """
        Создание нового метода для добавления или удаления сервисов
        """
        # Получаем текущую запись
        pws = await self.get_one_ore_none(**filter_by)

        if not pws:
            raise ValueError("Запись не найдена")

        # Подготовка данных для обновления
        update_data = data.model_dump(exclude_unset=exclude_unset)
        service_ids = update_data.pop("service_ids", None)

        # Определяет актуальные service_ids
        final_service_ids = (
            service_ids
            if service_ids is not None
            else (
                [int(sid) for sid in pws.service_ids.split(",")]
                if pws.service_ids
                else []
            )
        )

        # Вычисляем сумму услуг
        sum_services = 0
        if final_service_ids:
            stmt = select(ServicesORM.price).where(
                ServicesORM.id.in_(final_service_ids)
            )
            result = await self.session.execute(stmt)
            services_prices = result.scalars().all()
            # if len(services_prices) != len(final_service_ids):
            #     raise ValueError("Одна или несколько услуг не найдены")
            sum_services = sum(services_prices)

        # Получаем цену продукта
        product_id = update_data.get("product_id")
        product = await self.session.get(ProductsORM, product_id)
        product_price = product.price

        update_data["price"] = product_price + sum_services
        update_data["service_ids"] = final_service_ids

        # Обновляем основную таблицу
        await self.edit(
            data=ProductsWithServicesAdd(**update_data),
            exclude_unset=True,
            **filter_by,
        )
        # Обновляем связи многие-ко-многим
        if service_ids is not None:
            await self.session.execute(
                delete(ProductsWithServicesServices).where(
                    ProductsWithServicesServices.product_with_service_id == pws.id
                )
            )
            if final_service_ids:
                await self.session.execute(
                    insert(ProductsWithServicesServices).values(
                        [
                            {"product_with_service_id": pws.id, "service_id": sid}
                            for sid in final_service_ids
                        ]
                    )
                )

        await self.session.commit()
