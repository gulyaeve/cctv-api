from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from app.database import async_session_maker
from app.classrooms.models import ClassroomModel
from app.dao.base import BaseDAO
from app.logger import logger


class ClassroomsDAO(BaseDAO):
    model = ClassroomModel

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        try:
            query = select(
                ClassroomModel
            ).filter_by(
                **filter_by
            ).options(
                joinedload(ClassroomModel.classroom_type)
            )
            async with async_session_maker() as session:
                result = await session.execute(query)
                return result.scalars().one_or_none()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Data not found"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Data not found"

            logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            return None
        
    @classmethod
    async def find_all(cls, **filter_by):
        try:
            query = select(
                ClassroomModel,
            ).filter_by(
                **filter_by
            ).options(
                joinedload(ClassroomModel.classroom_type)
            ).order_by(
                ClassroomModel.id
            )
            async with async_session_maker() as session:
                result = await session.execute(query)
                return result.scalars().all()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Data not found"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Data not found"

            logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            return None