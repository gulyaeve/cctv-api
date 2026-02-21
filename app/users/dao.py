from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.logger import logger
from app.database import async_session_maker
from app.dao.base import BaseDAO
from app.users.models import Permission, Role, UserModel, role_permissions, user_roles


class UsersDAO(BaseDAO):
    model = UserModel


class RolesDAO(BaseDAO):
    model = Role


class PermissionDAO(BaseDAO):
    model = Permission
    
    @classmethod
    async def check_user_permissions(cls, user_id: int, permission_name: str):
        try:
            count = select(
                    Permission, role_permissions, user_roles
                ).join(
                    role_permissions, Permission.id == role_permissions.c.permisson_id
                ).join(
                    user_roles, role_permissions.c.role_id == user_roles.c.role_id
                ).filter(
                Permission.name == permission_name, user_roles.c.user_id == user_id
            )
            async with async_session_maker() as session:
                result = await session.execute(count)
                await session.commit()
                return result.mappings().one_or_none()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot get data"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot get data"

            logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            return None
