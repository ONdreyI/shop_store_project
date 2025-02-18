from typing import List

from sqlalchemy import select

from src.models import CategoriesORM
from src.models import ProductsORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import ProductsMapper, ProductWithCategoryMapper
from src.schemas.products import ProductWithCategoryResponse
from src.logging_config import logger


class ProductsRepository(BaseRepository):
    model = ProductsORM
    mapper = ProductsMapper

    async def get_products_with_categories(self, product_id):
        logger.debug("Fetching product with ID: {product_id}")

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
        logger.debug(f"Generated query: {query}")

        try:
            # Выполняем запрос
            result = await self.session.execute(query)
            rows = result.mappings().all()
            logger.debug(f"Query result: {rows}")

            if not rows:
                logger.warning(f"No product found with ID: {product_id}")
                return None

            # Преобразуем каждую строку в доменную сущность через маппер
            mapped_result = ProductWithCategoryMapper.map_to_domain_entity(rows[0])
            logger.debug(f"Mapped result: {mapped_result}")
            return mapped_result

        except Exception as e:
            logger.error(f"Error fetching product with ID {product_id}: {e}")
            raise

    async def get_products_by_category(
        self, category_id: int, page: int = 1, per_page: int = 10
    ) -> List[ProductWithCategoryResponse]:
        """
        Формируем запрос с объединением таблиц и фильтрацией по category_id и пагинацией
        """
        query = (
            select(
                self.model.name.label("product_name"),
                CategoriesORM.name.label("category_name"),
                self.model.price,
                self.model.id.label("product_id"),
            )
            .join(CategoriesORM, self.model.category_id == CategoriesORM.id)
            .filter(CategoriesORM.id == category_id)
        )

        # Добавляем пагинацию
        offset = (page - 1) * per_page
        query = query.limit(per_page).offset(offset)

        print(f"query: {query}")

        # Выполняем запрос
        result = await self.session.execute(query)

        # Получаем результаты и сериализуем их с помощью Pydantic
        products = result.mappings().all()
        print(f"products ка список словарей: {products}")
        return [ProductWithCategoryResponse(**product) for product in products]

    async def get_product_price(self, product_id):
        query = select(ProductsORM.price).where(ProductsORM.id == product_id)
        result = await self.session.execute(query)
        product_price = result.scalar()
        return product_price
