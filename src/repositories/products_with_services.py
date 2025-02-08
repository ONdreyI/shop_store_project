from typing import List

from sqlalchemy import select, delete, insert, update

from repositories.base import BaseRepository
from src.models import ProductsORM
from src.models import ServicesORM
from src.models.products_with_services import (
    ProductsWithServicesORM,
    ProductsWithServicesServices,
)
from src.schemas.products_with_services import (
    ProductsWithServices,
    ProductsWithServicesPatch,
)


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

    async def get_all_pws(
        self,
        page: int,
        per_page: int,
    ) -> List[ProductsWithServices]:
        query = select(self.model)
        offset = (page - 1) * per_page
        query = query.limit(per_page).offset(offset)
        result = await self.session.execute(query)
        products_with_services = []
        for model in result.scalars().all():
            # Преобразуем строку service_ids в список перед валидацией
            if model.service_ids:
                model.service_ids = [int(sid) for sid in model.service_ids.split(",")]
            products_with_services.append(ProductsWithServices.from_orm(model))
        return products_with_services

    async def edit_pws(
        self,
        data: ProductsWithServicesPatch,  # Используем вашу схему PATCH
        exclude_unset: bool = False,
        **filter_by,
    ) -> None:
        """
        Обновляет запись в products_with_services и связанные сервисы.
        """
        # Обновляем основные поля (product_id, price)
        update_data = data.model_dump(exclude_unset=exclude_unset)

        # Удаляем service_ids из update_data, чтобы не обновлять его напрямую
        service_ids = update_data.pop("service_ids", None)

        # Обновляем основную таблицу
        if update_data:
            await self.edit(
                data=ProductsWithServicesPatch(**update_data),
                exclude_unset=exclude_unset,
                **filter_by,
            )

        # Обрабатываем сервисы, если они переданы
        if service_ids is not None:
            # Получаем ID записи
            pws = await self.get_one_ore_none(**filter_by)
            if not pws:
                raise ValueError("Запись не найдена")

            # Удаляем старые связи
            delete_stmt = delete(ProductsWithServicesServices).where(
                ProductsWithServicesServices.product_with_service_id == pws.id
            )
            await self.session.execute(delete_stmt)

            # Добавляем новые связи
            if service_ids:
                insert_values = [
                    {"product_with_service_id": pws.id, "service_id": sid}
                    for sid in service_ids
                ]
                insert_stmt = insert(ProductsWithServicesServices).values(insert_values)
                await self.session.execute(insert_stmt)

            # Обновляем поле service_ids (если нужно хранить строку)
            await self.session.execute(
                update(ProductsWithServicesORM)
                .where(ProductsWithServicesORM.id == pws.id)
                .values(
                    service_ids=",".join(map(str, service_ids)) if service_ids else None
                )
            )

            await self.session.commit()
