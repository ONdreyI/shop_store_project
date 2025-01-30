import logging

from fastapi import APIRouter, HTTPException, Response, Request
from pydantic import ValidationError

from app.dependencies import UserIdDep
from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd, UserLogin
from src.services.auth import AuthService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["Авторизация и аутентификация"],
)


@router.post("/register", name="Аутентификация")
async def register_user(data: UserRequestAdd):
    hashed_password = AuthService().pwd_context.hash(data.password)
    new_user_data = UserAdd(
        username=data.username,
        email=data.email,
        hashed_password=hashed_password,
        role_id=data.role_id,
    )
    async with async_session_maker() as session:
        try:
            await UsersRepository(session).add(new_user_data)
            await session.commit()
            return {"status": "OK"}
        except ValidationError as e:
            raise HTTPException(status_code=401, detail=e.error())


@router.post("/login", name="Авторизация")
async def login_user(
    data: UserLogin,
    response: Response,
):
    async with async_session_maker() as session:
        logger.info(f"Searching for user with email: {data.email}")
        user = await UsersRepository(session).get_user_with_hashed_password(
            email=data.email
        )
        logger.info(f"User found: {user}")
        if not user:
            raise HTTPException(
                status_code=401, detail="Пользователь с таким email не зарегистрирован"
            )
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Пароль неверный")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}


@router.get("/me", name="Получение данных о пользователе")
async def only_auth(user_id: UserIdDep):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_ore_none(id=user_id)
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь не авторизован")
        return {"status": "OK", "user": user}


@router.post(
    "/logout",
    name="Выход из системы!",
)
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK", "details": "Выход из системы успешен"}
