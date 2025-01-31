from typing import Annotated

from fastapi import Request, HTTPException, Depends

from src.database import async_session_maker
from src.services.auth import AuthService
from src.utils.db_manager import DBManager


def get_token(request: Request):
    token = request.cookies.get("access_token", None)
    if token is None:
        raise HTTPException(status_code=401, detail="Вы не предоставили токен доступа")


def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().decode_jwt_token(token)
    return data["user_id"]


UserIdDep = Annotated[int, Depends(get_current_user_id)]


def get_db_manager():
    return DBManager(session_factory=async_session_maker)


async def get_db():
    async with get_db_manager() as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
