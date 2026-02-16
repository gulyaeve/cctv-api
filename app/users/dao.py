from sqlalchemy import select
from app.database import async_session_maker
from app.dao.base import BaseDAO
from app.users.models import Permission, Role, UserModel


class UsersDAO(BaseDAO):
    model = UserModel

    @classmethod
    async def find_users_with_role(cls, role: str):
        query = select(UserModel).where(UserModel.roles.any(Role.name == role))
        async with async_session_maker() as session:
            result = await session.execute(query)
            return result.scalars().all()


    @classmethod
    async def find_users_with_permissions(cls, permission: str):
        query = select(UserModel).where(UserModel.roles.any(Role.permissions.any(Permission.name == permission)))
        async with async_session_maker() as session:
            result = await session.execute(query)
            return result.scalars().all()



class RolesDAO(BaseDAO):
    model = Role

    @classmethod
    async def find_roles_with_permission(cls, permission: str):
        query = select(Role).where(Role.permissions.any(Permission.name == permission))
        async with async_session_maker() as session:
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_user_roles(cls, user_id: int):
        query = select(Role).where(Role.users.any(UserModel.id == user_id))
        async with async_session_maker() as session:
            result = await session.execute(query)
            return result.scalars().all()


class PermissionDAO(BaseDAO):
    model = Permission

