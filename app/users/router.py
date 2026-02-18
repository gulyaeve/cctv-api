from datetime import datetime, timedelta, timezone
import logging
from typing import Optional, Sequence, Annotated
from fastapi import APIRouter, Depends, Form, Query, Response, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
# from fastapi_login import LoginManager
from pydantic import EmailStr


from app.users.auth import auth_user, get_password_hash, create_token
from app.users.dependencies import get_current_user
# from app.users.models import UserModel
from app.users.schemas import UserScheme, UserSearch
from app.users.dao import UsersDAO
from app.exceptions import UserExistException
from app.config import settings
# from fastapi_cache.decorator import cache


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

# manager = LoginManager(
#     settings.SECRET_KEY,
#     token_url=f"{router.prefix}/login",
#     not_authenticated_exception=NotAuthenticatedException,
#     use_cookie=True
#     )


# @manager.user_loader()
# async def load_user(email: str):
#     user: UserModel = await UsersDAO.find_one_or_none(email=email)
#     return user


@router.get("", dependencies=[Depends(get_current_user)])
# @cache(expire=60)
async def get_all_users(filter_query: Annotated[UserSearch, Query()]) -> Sequence[UserScheme]:
    """
    Get all users
    """
    filter_model = filter_query.model_dump(exclude_unset=True, exclude_defaults=True)
    return await UsersDAO.find_all(**filter_model)


@router.post("/register", status_code=201)
async def register_user(
    email: Annotated[EmailStr, Form()],
    password: Annotated[str, Form()],
    username: Annotated[str, Form()],
    ):
    existing_user = await UsersDAO.find_one_or_none(email=email)
    if existing_user:
        raise UserExistException
    await UsersDAO.add(
        email=email,
        hashed_password=get_password_hash(password),
        username=username
    )
    logging.info(f"User saved to db: {email}")


# @router.post("/token")
# async def check_token(data: OAuth2PasswordRequestForm = Depends()):
#     email = data.username
#     password = data.password

#     user = await load_user(email)
#     logging.info(f"{data.__dict__=} {user=}")
#     if not user:
#         raise InvalidCredentialsException
#     elif not verify_password(password, user.hashed_password):
#         raise InvalidCredentialsException

#     access_token = manager.create_access_token(
#         data=dict(sub=email),
#         expires=(timedelta(minutes=settings.TOKEN_TTL_MINUTES))
#     )
#     return {'access_token': access_token, 'token_type': 'bearer'}


# @router.post("/login")
# async def login_user(response: Response, user_data: UserLogin):
#     user = await auth_user(user_data.email, user_data.password)
#     access_token = create_token({"sub": str(user.id)})
#     response.set_cookie(key="access_token", value=access_token)
#     # return {"access_token": access_token}

# @router.post("/login")
# async def login_user(
#     response: Response,
#     data: OAuth2PasswordRequestForm = Depends()
# ):
#     user = await auth_user(data.username, data.password)
#     access_token = create_token({"sub": str(user.id)})
#     response.set_cookie(key="access_token", value=access_token)
#     return {"access_token": access_token}

@router.post("/login")
async def login_user(
    response: Response,
    data: OAuth2PasswordRequestForm = Depends()
):
    user = await auth_user(data.username, data.password)
    if not user:
        return RedirectResponse("/login")
    access_token = create_token({"sub": str(user.id)})
    response = RedirectResponse("/active_monitoring", status_code=status.HTTP_302_FOUND)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        expires=datetime.now(timezone.utc) + timedelta(hours=settings.TOKEN_TTL_MINUTES)
        )
    return response


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")


@router.get("/me")
async def user_get_itself(current_user = Depends(get_current_user)) -> UserScheme:
    return current_user
    

@router.get("/{id}")
async def get_user_info(id: int, current_user = Depends(get_current_user)) -> Optional[UserScheme]:
    return await UsersDAO.find_one_or_none(id=id)
