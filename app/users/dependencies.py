from typing import Callable, Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials
from httpx import AsyncClient
from jose import JWTError, jwt

from app.config import settings
from app.exceptions import (
    OperationNotPermited,
    TokenIncorrect,
    TokenMissing,
    UserNotPresent,
)
from app.users.auth import get_bearer_token, known_tokens
from app.users.dao import PermissionDAO, RolesDAO, UsersDAO
from app.users.models import UserModel
from app.utils.keycloak_client import KeycloakClient

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)


def get_token(request: Request):
    return request.cookies.get("jwt_access_token")


def get_keycloak_token(request: Request):
    return request.cookies.get("access_token")


# Получаем KeycloakClient из app.state
def get_keycloak_client(request: Request) -> KeycloakClient:
    return request.app.state.keycloak_client


async def get_current_user(
    jwt_token: Optional[str] = Depends(get_token),
    keycloak_token: Optional[str] = Depends(get_keycloak_token),
    bearer_auth: Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token),
    keycloak: Optional[KeycloakClient] = Depends(get_keycloak_client),
):
    if jwt_token is not None:
        try:
            payload = jwt.decode(
                jwt_token,
                settings.SECRET_KEY,
                settings.ALGORITHM,
            )
        except JWTError:
            raise TokenIncorrect
        user_id: int = int(payload.get("sub"))
        if not user_id:
            raise UserNotPresent
        user = await UsersDAO.find_one_or_none(id=user_id)
        user = await UsersDAO.get_user(user_id)
        if not user:
            raise UserNotPresent
        return user
    if keycloak_token is not None and keycloak is not None:
        user_info = await keycloak.get_user_info(keycloak_token)
        user = await UsersDAO.find_one_or_none(keycloak_uuid=user_info.get("sub"))
        if not user:
            raise UserNotPresent
        return user
    if bearer_auth is not None:
        bearer_token = bearer_auth.credentials
        user = await UsersDAO.find_one_or_none(bearer_token=bearer_token)
        if user:
            return user
        if bearer_token in known_tokens:
            return await UsersDAO.find_one_or_none(id=1)
    raise TokenMissing


async def validate_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            settings.ALGORITHM,
        )
    except JWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    user_id: int = int(payload.get("sub"))
    if not user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    user = await UsersDAO.find_one_or_none(id=user_id)
    # user = await UsersDAO.get_user(user_id)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    return user


async def validate_keycloak_token(keycloak_token: str):
    headers = {"Authorization": f"Bearer {keycloak_token}"}
    async with AsyncClient() as client:
        response = await client.get(settings.userinfo_url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)
        user_info = response.json()
        user = await UsersDAO.find_one_or_none(keycloak_uuid=user_info.get("sub"))
        if not user:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)
        return user


async def get_fake_user():
    return await UsersDAO.find_one_or_none(id=1)


def permission_required(permission: str) -> Callable:
    async def permission_checker(current_user: UserModel = Depends(get_current_user)):
        check_superadmin_role = await RolesDAO.check_user_role(
            current_user.id, "superadmin"
        )
        if check_superadmin_role:
            return True

        check_permission = await PermissionDAO.check_user_permissions(
            current_user.id, permission
        )
        if not check_permission:
            raise OperationNotPermited
        else:
            return check_permission

    return permission_checker


async def permission_checker(user_id: int, permission: str):
    check_permission = await PermissionDAO.check_user_permissions(user_id, permission)
    if not check_permission:
        raise OperationNotPermited
    else:
        return check_permission


def role_required(role: str) -> Callable:
    async def role_checker(current_user: UserModel = Depends(get_current_user)):
        check_role = await RolesDAO.check_user_role(current_user.id, role)
        if not check_role:
            raise OperationNotPermited
        else:
            return check_role

    return role_checker


async def role_checker(user_id: int, role: str):
    check_role = await RolesDAO.check_user_role(user_id, role)
    if not check_role:
        raise OperationNotPermited
    else:
        return check_role
