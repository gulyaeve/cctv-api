import logging
from typing import Callable, Optional, Sequence
from fastapi import Depends, Request
from jose import jwt, JWTError
from app.exceptions import OperationNotPermited, TokenMissing, TokenIncorrect, UserNotPresent
from app.config import settings
from app.users.dao import RolesDAO, UsersDAO
from app.users.models import UserModel


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


# async def get_current_user_roles(current_user: UserModel = Depends(get_current_user)):
#     return await RolesDAO.find_user_roles(user_id=current_user.id)
#
#
# async def check_current_user_permissions(permission: str, current_user: UserModel = Depends(get_current_user)):
#     return await UsersDAO.find_users_with_permission(permission)


# def role_required(roles: Sequence[str]):
#     def role_checker(current_user: UserModel = Depends(get_current_user)):
#         if not any(role.name in roles for role in current_user.roles):
#             raise OperationNotPermited
#         return current_user
#     return role_checker


# async def permission_required(permission: str):
#     test = await UsersDAO.check_user_permisson()
#     logging.info(f"{test}")
#     async def permission_checker(current_user: UserModel = Depends(get_current_user)):
#         logging.info(f"{current_user}")
#         permissions = [perm.name for role in current_user.roles for perm in role.permissions]
#         if permission not in permissions:
#             raise OperationNotPermited
#         return current_user
#     return permission_checker


# def permission_checker(permission: str) -> Callable:
#     async def user_checker(check_current_user_permission: Optional[UserModel] = Depends(check_current_user_permission(permission))):
#         if not check_current_user_permission:
#             raise OperationNotPermited
        # logging.info(current_user_roles)
        # roles_with_permission = await RolesDAO.find_roles_with_permission(permission=permission)
        # logging.info(roles_with_permission)
        # users_with_pepermission = await UsersDAO.find_users_with_permission(permission)
        # logging.info(users_with_pepermission)
        # raise OperationNotPermited
        # return user
        # for role in roles_with_permission:
            # users_with_role = await UsersDAO.find_users_with_role(role.name)
            # for user in users_with_role:
            #     if user.id == current_user.id:
            #         return current_user
            #     else:
            #         raise OperationNotPermited
    # return user_checker
            
