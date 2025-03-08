import sys
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import uvicorn

sys.path.append(str(Path(__file__).parent.parent))

from src.logging_config import logger  # noqa: E402
from src.init import redis_manager  # noqa: E402
from src.app.services import router as router_service  # noqa: E402
from src.app.auth import router as router_auth  # noqa: E402
from src.app.categories import router as router_category  # noqa: E402
from src.app.customers import router as router_customer  # noqa: E402
from src.app.managers import router as router_manager  # noqa: E402
from src.app.regions import router as router_region  # noqa: E402
from src.app.products import router as router_product  # noqa: E402
from src.app.orders import router as router_order  # noqa: E402
from src.app.materialized_views import router as router_mv  # noqa: E402


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Start APP")
    try:
        await redis_manager.connect()
        logger.info("Successfully connected to Redis")
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
    FastAPICache.init(
        RedisBackend(redis_manager._redis),
        prefix="fastapi-cache",
    )
    yield
    logger.info("Restart APP")
    await redis_manager.close()


app = FastAPI(lifespan=lifespan)


@app.get("/")
def func():
    return {"message": "Welcome to the SHOP-STORE!"}


app.include_router(router_auth)
app.include_router(router_service)
app.include_router(router_category)
app.include_router(router_product)
app.include_router(router_manager)
app.include_router(router_region)
app.include_router(router_customer)
app.include_router(router_order)
app.include_router(router_mv)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="localhost")
