
from typing import Callable
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.exceptions import OperationNotPermited, TokenMissing, TokenIncorrect, UserNotPresent
from app.config import settings
from app.users.dao import PermissionDAO, RolesDAO, UsersDAO
from app.users.models import UserModel


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)


def get_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise TokenMissing
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            settings.ALGORITHM,
        )
    except JWTError:
        raise TokenIncorrect
    user_id: int = int(payload.get("sub"))
    if not user_id:
        raise UserNotPresent
    user = await UsersDAO.find_one_or_none(id=user_id)
    if not user:
        raise UserNotPresent
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
