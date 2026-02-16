import logging
from sqlalchemy import select
from app.database import async_session_maker
from app.classrooms.models import ClassroomModel
from app.dao.base import BaseDAO
from app.groups.models import GroupModel
from app.incidents.models import IncidentModel
from app.schedule.models import ScheduleModel
from app.teachers.models import TeacherModel
from app.users.models import UserModel
from sqlalchemy.exc import SQLAlchemyError


class IncidentsDAO(BaseDAO):
    model = IncidentModel

    @classmethod
    async def get_incidents_info(cls, visor_id: int, event_id: int):
        try:
            query = (
                select(
                    IncidentModel,
                    TeacherModel.name.label('current_teacher'),
                    GroupModel.name.label('current_group'),
                    ScheduleModel.subject.label('current_schedule'),
                    ClassroomModel.name.label('current_classroom'),
                    UserModel.full_name.label('current_visor')
                )
                .join(ScheduleModel, IncidentModel.event == ScheduleModel.id)
                .join(ClassroomModel, ScheduleModel.classroom_id == ClassroomModel.id)
                .join(TeacherModel, ScheduleModel.teacher_id == TeacherModel.id)
                .join(GroupModel, ScheduleModel.group_id == GroupModel.id)
                .join(UserModel, IncidentModel.visor_id == UserModel.id)
                .filter(IncidentModel.visor_id == visor_id, IncidentModel.event == event_id)
            )
            async with async_session_maker() as session:
                    result = await session.execute(query)
                    return result.mappings().one_or_none()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Data not found"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Data not found"

            logging.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            return None