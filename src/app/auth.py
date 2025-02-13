import logging

from fastapi import APIRouter, HTTPException, Response
from pydantic import ValidationError

from app.dependencies import UserIdDep, DBDep
from src.schemas.users import UserRequestAdd, UserAdd, UserLogin
from src.services.auth import AuthService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["Авторизация и аутентификация"],
)


@router.post("/register", name="Аутентификация")
async def register_user(
    data: UserRequestAdd,
    db: DBDep,
):
    hashed_password = AuthService().pwd_context.hash(data.password)
    new_user_data = UserAdd(
        username=data.username,
        email=data.email,
        hashed_password=hashed_password,
        role_id=data.role_id,
    )
    try:
        await db.users.add(new_user_data)
        await db.commit()
        return {"status": "OK"}
    except ValidationError as e:
        raise HTTPException(status_code=401, detail=e.error())


@router.post("/login", name="Авторизация")
async def login_user(
    data: UserLogin,
    response: Response,
    db: DBDep,
):
    logger.info(f"Searching for user with email: {data.email}")
    user = await db.users.get_user_with_hashed_password(email=data.email)
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


@router.get(
    "/me",
    name="Получение данных о пользователе",
    description="Получение данных о пользователе",
)
async def only_auth(user_id: UserIdDep, db: DBDep):
    user = await db.users.get_one_ore_none(id=user_id)
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
