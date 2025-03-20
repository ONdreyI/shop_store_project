from datetime import timedelta, datetime, timezone

import jwt
from fastapi import HTTPException
from passlib.context import CryptContext

from src.config import settings
from src.logging_config import logger


class AuthService:

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str:
        logger.info("Создание токена доступа с данными: %s", data)
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        logger.info("Токен доступа успешно создан.")
        return encoded_jwt

    def hash_password(self, password: str) -> str:
        logger.info("Хеширование пароля.")
        hashed_password = self.pwd_context.hash(password)
        logger.info("Пароль успешно захеширован.")
        return hashed_password

    def verify_password(self, plain_password, hashed_password) -> bool:
        logger.info("Проверка пароля.")
        is_verified = self.pwd_context.verify(plain_password, hashed_password)
        logger.info("Результат проверки пароля: %s", is_verified)
        return is_verified

    def decode_jwt_token(self, token: str) -> dict:
        logger.info("Декодирование JWT токена.")
        try:
            decoded_token = jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
            logger.info("JWT токен успешно декодирован.")
            return decoded_token
        except jwt.exceptions.DecodeError:
            logger.error("Обнаружен неверный токен.")
            raise HTTPException(status_code=401, detail="Неверный токен!")
