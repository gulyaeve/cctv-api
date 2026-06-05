from datetime import datetime

from sqlalchemy import and_, insert, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload

from app.dao.base import BaseDAO
from app.exceptions import ObjectMissingException
from app.groups.models import GroupModel
from app.database import async_session_maker
from app.logger import logger
from app.schedule.models import ScheduleModel
from app.teachers.models import TeacherModel



class GroupsDAO(BaseDAO):
    model = GroupModel

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        try:
            query = select(
                GroupModel
            ).filter_by(
                **filter_by
            ).options(
                selectinload(GroupModel.teacher)
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
                GroupModel,
            ).filter_by(
                **filter_by
            ).options(
                selectinload(GroupModel.teacher)
            ).order_by(
                GroupModel.id
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

    @classmethod
    async def add(cls, **data):
        try:
            query = insert(cls.model).values(**data)
            async with async_session_maker() as session:
                await session.execute(query)
                await session.commit()
                # return result.scalar_one_or_none()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot insert data into table"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot insert data into table"

            logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            return None

    @classmethod
    async def add_bulk(cls, *data):
        try:
            query = insert(cls.model).values(*data)
            async with async_session_maker() as session:
                await session.execute(query)
                await session.commit()
                # return result.mappings().all()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc"
            elif isinstance(e, Exception):
                msg = "Unknown Exc"
            msg += ": Cannot bulk insert data into table"

            logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            return None
        
    @classmethod
    async def update(cls, id: int, **data):
        try:
            query = (
                update(cls.model)
                .where(cls.model.id == id)
                .values(**data)
                # .returning(cls.model)
                )
            async with async_session_maker() as session:
                await session.execute(query)
                await session.commit()
                # return result.scalar_one_or_none()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot update data in table"
                raise ObjectMissingException
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot update data in table"

            logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            return None

    @classmethod
    async def find_schedule_for_group(cls, id: int, timestamp: datetime = datetime.now()):
        try:
            query = select(
                GroupModel.__table__,
                ScheduleModel.id.label('schedule_id'),
                ScheduleModel.subject.label('schedule_subject'),
                ScheduleModel.classroom_id.label('classroom_id'),
                ScheduleModel.timestamp_start.label('schedule_timestamp_start'),
                ScheduleModel.timestamp_end.label('schedule_timestamp_end'),
                TeacherModel.name.label('teacher_name'),
            ).join(
                ScheduleModel, GroupModel.id == ScheduleModel.group_id,
            ).join(
                TeacherModel, ScheduleModel.teacher_id == TeacherModel.id,
            ).filter(
                and_(
                    ScheduleModel.timestamp_start <= timestamp,
                    timestamp <= ScheduleModel.timestamp_end,
                    GroupModel.id == id,
                )
            )
            async with async_session_maker() as session:
                result = await session.execute(query)
                return result.mappings().all()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Data not found"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Data not found"

            logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            return None

