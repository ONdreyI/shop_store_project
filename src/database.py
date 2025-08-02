from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from src.config import settings

engine = create_async_engine(settings.DB_URL)
engine_null_pool = create_async_engine(
    settings.DB_URL,
    poolclass=NullPool,
)

async_session_maker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)
async_session_maker_null_pool = async_sessionmaker(
<<<<<<< HEAD
    bind=engine_null_pool,
    expire_on_commit=False,
=======
    bind=engine_null_pool, expire_on_commit=False
>>>>>>> 42d8a6137fd0e22eef098d5eabd90c6a81366444
)


class Base(DeclarativeBase):
    pass
