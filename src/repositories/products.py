from typing import List

from sqlalchemy import select

from src.models import CategoriesORM
from src.repositories.base import BaseRepository
from src.schemas.products import ProductWithCategoryResponse
from src.models import ProductsORM
from src.repositories.mappers.mappers import ProductsMapper, ProductWithCategoryMapper


class ProductsRepository(BaseRepository):
    model = ProductsORM
    mapper = ProductsMapper

    async def get_products_with_categories(self, product_id):
        # Формируем запрос с объединением таблиц
        query = (
            select(
                self.model.name.label("product_name"),
                CategoriesORM.name.label("category_name"),
                self.model.price,
                self.model.id.label("product_id"),
            )
            .join(CategoriesORM, self.model.category_id == CategoriesORM.id)
            .filter(ProductsORM.id == product_id)
        )
        print(f"query: {query}")

        # Выполняем запрос
        result = await self.session.execute(query)

        # Получаем все строки как список кортежей
        rows = result.mappings().all()
        print(rows)

        if not rows:
            return None

        # Преобразуем каждую строку в доменную сущность через маппер
        # return ProductWithCategoryResponse.model_validate(rows[0])
        return ProductWithCategoryMapper.map_to_domain_entity(rows[0])


