import datetime
from datetime import timedelta, timezone
from enum import Enum, auto

import jwt
# import passlib.context
from fastapi import HTTPException, Depends
from fastapi.openapi.models import OAuth2
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from core import config

auth_scheme = OAuth2PasswordBearer(tokenUrl="security/")


# class PasswordManager:
#     _context = passlib.context.CryptContext(schemes=["bcrypt"], deprecated="auto")
#
#     @classmethod
#     def hash(cls, password: str) -> str:
#         return cls._context.hash(password)
#
#     @classmethod
#     def verify(cls, plain: str, hashed_str: str) -> bool:
#         return cls._context.verify(plain, hashed_str)


class TokenTypes(Enum):
    ACCESS = auto()
    REFRESH = auto()


class TokenManager:
    _ALGORITHM = "HS256"
    _TOKEN_SECRET_KEY = config.settings.TOKEN_SECRET_KEY
    ACCESS_TOKEN_EXPIRE_MINUTES = config.settings.ACCESS_TOKEN_EXPIRE_MINUTES
    REFRESH_TOKEN_EXPIRE_HOURS = config.settings.REFRESH_TOKEN_EXPIRE_HOURS

    @classmethod
    def create(cls, data: dict, token_type: TokenTypes) -> str:
        to_encode = data.copy()
        expire_delta = timedelta(
            minutes=cls.ACCESS_TOKEN_EXPIRE_MINUTES) if token_type is TokenTypes.ACCESS else timedelta(
            hours=cls.REFRESH_TOKEN_EXPIRE_HOURS)
        expire = datetime.datetime.now(tz=timezone.utc) + expire_delta
        to_encode.update({"exp": expire})
        try:
            jwt_str = jwt.encode(to_encode, cls._TOKEN_SECRET_KEY, cls._ALGORITHM)
            return jwt_str
        except:
            print("token not created!")

    @classmethod
    def decode(cls, token: str = Depends(auth_scheme)) -> int:
        try:
            payload: dict = jwt.decode(token, cls._TOKEN_SECRET_KEY, cls._ALGORITHM, options={"verify_sub": False})
            address = payload.get("sub")
            if address is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
            return address
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="токен просрочен")
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
