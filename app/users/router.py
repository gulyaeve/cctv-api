from datetime import datetime, timedelta, timezone
from app.logger import logger
from typing import Optional, Sequence, Annotated
from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request, Response, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
# from fastapi_login import LoginManager
from pydantic import EmailStr, SecretStr


from app.users.auth import auth_user, get_password_hash, create_token, verify_password
from app.users.dependencies import get_current_user, permission_required, validate_token
# from app.users.models import UserModel
from app.users.schemas import MediaMTXPayload, UserScheme, UserSearch
from app.users.dao import UsersDAO
from app.exceptions import IncorrectEmailOrPassword, PasswordNotValidate, PasswordsDontMatchValidation, UserExistException, UserNotPresent
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


@router.get("", dependencies=[Depends(permission_required("superadmin"))])
async def get_all_users(
        filter_query: Annotated[UserSearch, Query()],
        current_user = Depends(get_current_user)
) -> Sequence[UserScheme]:
    """
    Get all users
    """
    logger.info(
        "Superadmin gets users list",
        extra=current_user,
        exc_info=True
    )
    filter_model = filter_query.model_dump(exclude_unset=True, exclude_defaults=True)
    return await UsersDAO.find_all(**filter_model)


@router.post("/register", status_code=201)
async def register_user(
    email: Annotated[EmailStr, Form()],
    request: Request,
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
    logger.info(
        "User registered and saved to db",
        extra={"email": email},
        exc_info=True
    )
    start_page = request.url_for("page_get_dashboard_page")
    response = RedirectResponse(start_page, status_code=status.HTTP_302_FOUND)
    return response


@router.post("/change_password", status_code=status.HTTP_200_OK, response_model=UserScheme)
async def change_password(
    old_password: Annotated[SecretStr, Form()],
    new_password_1: Annotated[SecretStr, Form(min_length=8)],
    new_password_2: Annotated[SecretStr, Form(min_length=8)],
    current_user = Depends(get_current_user),
):
    if new_password_1 != new_password_2:
        raise PasswordsDontMatchValidation
    if not new_password_1:
        raise PasswordNotValidate
    user = await UsersDAO.find_one_or_none(id=current_user.id)
    if not verify_password(old_password.get_secret_value(), user.hashed_password):
        raise IncorrectEmailOrPassword
    return await UsersDAO.update_password(current_user.id, get_password_hash(new_password_1.get_secret_value()))
    


@router.post("/login")
async def login_user(
    response: Response,
    request: Request,
    data: OAuth2PasswordRequestForm = Depends()
):
    user = await auth_user(data.username, data.password)
    if not user:
        raise UserNotPresent
    access_token = create_token({"sub": str(user.id)})
    start_page = request.url_for("page_get_dashboard_page")
    response = RedirectResponse(start_page, status_code=status.HTTP_302_FOUND)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=False,
        expires=datetime.now(timezone.utc) + timedelta(hours=settings.TOKEN_TTL_MINUTES)
        )
    logger.info(
        "User logged in",
        extra={"email": user.email},
        exc_info=True
    )
    return response


@router.post("/logout")
async def logout_user(response: Response, request: Request):
    response = RedirectResponse(request.url_for("page_get_login"), status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("access_token")
    return response


@router.get("/me")
async def user_get_itself(current_user = Depends(get_current_user)) -> UserScheme:
    logger.info(
        "User gets itself info",
        extra=current_user,
        exc_info=True
    )
    return current_user
    

@router.get("/{id}", dependencies=[Depends(permission_required("superadmin"))])
async def get_user_info(id: int, current_user = Depends(get_current_user)) -> Optional[UserScheme]:
    logger.info(
        "Superadmin gets user info",
        extra=current_user,
        exc_info=True
    )
    return await UsersDAO.find_one_or_none(id=id)


@router.post("/check_token")
async def check_token(payload: MediaMTXPayload):
    # logger.info(f"{payload=}")
    if payload.query == f"jwt={settings.TOKEN_BEARER}":
        # logger.info(f"{payload.query=} SUCCESS")
        raise HTTPException(status.HTTP_200_OK)
    if payload.token:
        # logger.info(f"{payload.token=}")
        return await validate_token(payload.token)
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
