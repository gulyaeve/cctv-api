from typing import Optional

from fastapi import Depends, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from pydantic import EmailStr
from jose import jwt
from datetime import datetime, timedelta

from app.logger import logger
from app.users.dao import UsersDAO
from app.exceptions import IncorrectEmailOrPassword, TokenIncorrect
from app.config import settings



pwd_context = CryptContext(schemes=["md5_crypt"], deprecated="auto")


known_tokens = {settings.TOKEN_BEARER}
get_bearer_token = HTTPBearer(auto_error=False)


async def auth_bearer_token(
    auth: Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token),
) -> str:
    if auth is None or (token := auth.credentials) not in known_tokens:
        raise TokenIncorrect
    return token


def noauth_handler(request: Request, exc):
    if "text/html" in request.headers.get("accept"):
        return RedirectResponse(
            url=request.url_for("page_get_login"),
            status_code=status.HTTP_303_SEE_OTHER
        )
    else:
        return JSONResponse(
            status_code=getattr(exc, "status_code"),
            content={"message": getattr(exc, "detail")}
        )


def noperm_handler(request, exc):
    if "text/html" in request.headers.get("accept"):
        return RedirectResponse(
            url=request.url_for("get_403_page"),
            status_code=status.HTTP_303_SEE_OTHER
        )
    else:
        return JSONResponse(
            status_code=getattr(exc, "status_code"),
            content={"message": getattr(exc, "detail")}
        )
    

def notfound_handler(request, exc):
    logger.warning(exc_info=True, extra={"message": getattr(exc, "detail")})
    if "text/html" in request.headers.get("accept"):
        return RedirectResponse(
            url=request.url_for("get_404_page"),
            status_code=status.HTTP_303_SEE_OTHER
        )
    else:
        return JSONResponse(
            status_code=getattr(exc, "status_code"),
            content={"message": getattr(exc, "detail")}
        )


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


async def auth_user(email: EmailStr, password: str):
    user = await UsersDAO.find_one_or_none(email=email)
    if not (user and verify_password(password, user.hashed_password)):
        raise IncorrectEmailOrPassword
    await UsersDAO.update(id=user.id, last_login=datetime.now())
    return user


def create_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(hours=settings.TOKEN_TTL_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        settings.ALGORITHM,
    )
    return encoded_jwt


# async def auth_checker(user = Depends(auth_user), token = Depends(auth_bearer_token)):
#     if not (user or token):
#         raise IncorrectEmailOrPassword



if __name__ == "__main__":
    ...
    # h = get_password_hash("Start123")
    # verify = verify_password("Start1234", h)
    # print(verify)
    # from asyncio import run
    # run(auth_user("vasya@example.com", "Start123"))
    # print(create_token({"test": 1}))
