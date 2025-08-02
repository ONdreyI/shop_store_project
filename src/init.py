import functools
import json
from typing import Callable

from src.connectors.redis_connector import RedisManager
from src.config import settings

redis_manager = RedisManager(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


def cache(expire: int = 3600):
    """
    Декоратор для кэширования результата асинхронной функции в Redis.
    :param expire: Время жизни кэша в секундах.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Фильтруем несериализуемые объекты
            non_serializable_types = {"DBManager", "AsyncSession", "Redis"}
            serializable_args = [
                arg
                for arg in args
                if not hasattr(arg, "__class__")
                or arg.__class__.__name__ not in non_serializable_types
            ]
            serializable_kwargs = {
                key: value
                for key, value in kwargs.items()
                if not hasattr(value, "__class__")
                or value.__class__.__name__ not in non_serializable_types
            }

            # Генерируем ключ
            try:
                cache_key = f"{func.__name__}:{json.dumps(serializable_args, sort_keys=True)}:{json.dumps(serializable_kwargs, sort_keys=True)}"
            except TypeError as e:
                raise ValueError(f"Failed to serialize arguments for cache key: {e}")

            # Проверяем кэш
            cached_result = await redis_manager.get(cache_key)
            if cached_result:
                return json.loads(cached_result.decode("utf-8"))

            # Выполняем функцию
            result = await func(*args, **kwargs)

            # Сохраняем в Redis
            if hasattr(result, "dict"):  # Pydantic модели
                serialized_result = json.dumps(result.dict())
            elif hasattr(result, "__dict__"):  # Обычные классы
                serialized_result = json.dumps(result.__dict__)
            else:
                serialized_result = json.dumps(result)  # Базовые типы
            await redis_manager.set(cache_key, serialized_result, expire=expire)
            return result

        return wrapper

    return decorator
