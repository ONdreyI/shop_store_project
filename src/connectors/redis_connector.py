import redis.asyncio as redis
from src.logging_config import logger


class RedisManager:
    _redis: redis.Redis

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self._redis = None  # Инициализируем _redis как None

    async def connect(self):
        try:
            logger.info(
                f"Начинаю подключение к Redis host={self.host}, port={self.port}"
            )
            self._redis = await redis.Redis(
                host=self.host, port=self.port, decode_responses=True
            )
            logger.info(
                f"Успешное подключение к Redis host={self.host}, port={self.port}"
            )
        except Exception as e:
            logger.error(f"Ошибка при подключении к Redis: {e}")
            raise

    async def set(self, key: str, value: str, expire: int | None = None):
        logger.debug(f"Установка значения для ключа '{key}' с expire={expire}")
        if expire:
            await self._redis.set(key, value, ex=expire)
        else:
            await self._redis.set(key, value)
        logger.debug(f"Значение для ключа '{key}' успешно установлено")

    async def get(self, key: str):
        if not self._redis:
            raise RuntimeError("Redis connection is not initialized")
        logger.debug(f"Получение значения для ключа '{key}'")
        value = await self._redis.get(key)
        logger.debug(f"Значение для ключа '{key}' получено: {value}")
        return value

    async def delete(self, key: str):
        logger.debug(f"Удаление ключа '{key}'")
        await self._redis.delete(key)
        logger.debug(f"Ключ '{key}' успешно удален")

    async def close(self):
        if self._redis:
            logger.info("Закрытие соединения с Redis")
            await self._redis.close()
            await self._redis.connection_pool.disconnect()
            logger.info("Соединение с Redis успешно закрыто")


# Пример использования:
# redis_manager = RedisManager(host="localhost", port=6379)
# await redis_manager.connect()
# await redis_manager.set("key", "value", expire=60)
# value = await redis_manager.get("key")
# await redis_manager.delete("key")
# await redis_manager.close()
