from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.logger import logger
from app.database import async_session_maker
from app.dao.base import BaseDAO
from app.users.models import Permission, Role, UserModel, role_permissions, user_roles


class UsersDAO(BaseDAO):
    model = UserModel

    @classmethod
    async def get_user(cls, user_id: int):
        try:
            # roles_query = (
            #     select(
            #         Role.__table__,
            #     )
            #     .join(user_roles, user_roles.c.user_id == user_id)
            #     # .filter(user_roles.c.user_id == user_id)
            # )
            # query = (
            #     select(
            #         UserModel.__table__,
            #         Role.name.label("role_name"),
            #         Role.display_name.label("role_display_name"),
            #     )
            #     .outerjoin(user_roles, user_roles.c.user_id == UserModel.id)
            #     .outerjoin(Role, user_roles.c.role_id == Role.id)
            #     .filter(UserModel.id == user_id)
            # )
            query = (
                select(
                    UserModel.id,
                    UserModel.email,
                    UserModel.full_name,
                    UserModel.username,
                    UserModel.time_created,
                    UserModel.last_login,
                    # UserModel.roles
                )
                .filter(UserModel.id == user_id)
            )
            async with async_session_maker() as session:
                result = await session.execute(query)
                # result = dict((await session.execute(query)).mappings().one_or_none())
                # result_roles = list((await session.execute(roles_query)).mappings().all())
                # result["roles"] = result_roles
                await session.commit()
                return result.mappings().one_or_none()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot get data"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot get data"

            logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            return None


class RolesDAO(BaseDAO):
    model = Role

    @classmethod
    async def check_user_role(cls, user_id: int, role_name: str):
        try:
            query = select(
                    Role.name, user_roles
                ).join(
                    user_roles, user_roles.c.role_id == Role.id
                ).filter(
                user_roles.c.user_id == user_id, Role.name == role_name
            )
            async with async_session_maker() as session:
                result = await session.execute(query)
                await session.commit()
                return result.mappings().one_or_none()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot get data"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot get data"

            logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            return None



class PermissionDAO(BaseDAO):
    model = Permission
    
    @classmethod
    async def check_user_permissions(cls, user_id: int, permission_name: str):
        try:
            query = select(
                    Permission, role_permissions, user_roles
                ).join(
                    role_permissions, Permission.id == role_permissions.c.permisson_id
                ).join(
                    user_roles, role_permissions.c.role_id == user_roles.c.role_id
                ).filter(
                Permission.name == permission_name, user_roles.c.user_id == user_id
            )
            async with async_session_maker() as session:
                result = await session.execute(query)
                await session.commit()
                return result.mappings().one_or_none()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot get data"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot get data"

            logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            return None
