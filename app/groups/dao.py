from datetime import datetime

from sqlalchemy import and_, select
from sqlalchemy.exc import SQLAlchemyError

from app.dao.base import BaseDAO
from app.groups.models import GroupModel
from app.database import async_session_maker
from app.logger import logger
from app.schedule.models import ScheduleModel
from app.teachers.models import TeacherModel



class GroupsDAO(BaseDAO):
    model = GroupModel

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

