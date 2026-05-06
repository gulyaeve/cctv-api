
from typing import Callable, Optional
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.exceptions import OperationNotPermited, TokenMissing, TokenIncorrect, UserNotPresent
from app.config import settings
from app.users.dao import PermissionDAO, RolesDAO, UsersDAO
from app.users.models import UserModel
from app.users.auth import get_bearer_token, known_tokens


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)


def get_token(request: Request):
    return request.cookies.get("access_token")

    
async def get_current_user(
        jwt_token: Optional[str] = Depends(get_token),
        bearer_auth: Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token)
    ):
    if jwt_token:
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
        # user = await UsersDAO.find_one_or_none(id=user_id)
        user = await UsersDAO.get_user(user_id)
        if not user:
            raise UserNotPresent
        return user
    if bearer_auth:
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


async def get_fake_user():
    return await UsersDAO.find_one_or_none(id=1)


def permission_required(permission: str) -> Callable:
    async def permission_checker(current_user: UserModel = Depends(get_current_user)):
        check_superadmin_role = await RolesDAO.check_user_role(current_user.id, "superadmin")
        if check_superadmin_role:
            return True

        check_permission = await PermissionDAO.check_user_permissions(current_user.id, permission)
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
