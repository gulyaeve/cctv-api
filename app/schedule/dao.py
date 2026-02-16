import logging
from sqlalchemy import and_, desc, func, select, or_, text
from sqlalchemy.exc import SQLAlchemyError
from app.buildings.models import BuildingModel
from app.classrooms.models import ClassroomModel
from app.groups.models import GroupModel
from app.incidents.models import IncidentModel
from app.schedule.models import ScheduleModel
from app.dao.base import BaseDAO
from app.teachers.models import TeacherModel
from app.database import async_session_maker


class ScheduleDAO(BaseDAO):
    model = ScheduleModel

    @classmethod
    async def get_schedule_for_active_monitoring(cls, visor_id: int):
        try:
            inc_subquery = (
                select(
                    IncidentModel.event,
                    IncidentModel.status,
                    IncidentModel.time_created
                )
                .where(IncidentModel.visor_id == visor_id)
                .distinct(IncidentModel.event)
                .order_by(
                    IncidentModel.event,
                    desc(IncidentModel.time_created)
                )
            ).subquery('inc')

            # Основной запрос
            query = (
                select(
                    ScheduleModel.subject.label('current_subject'),
                    ScheduleModel.timestamp_start,
                    ScheduleModel.timestamp_end,
                    TeacherModel.name.label('current_teacher'),
                    ClassroomModel.name.label('current_classroom'),
                    ClassroomModel.id.label('current_classroom_id'),
                    BuildingModel.name.label('current_building'),
                    GroupModel.name.label('current_group'),
                    func.coalesce(inc_subquery.c.status, 1).label('last_status_incident'),
                    inc_subquery.c.time_created.label('time_created_incident')
                )
                .select_from(ScheduleModel)
                .join(TeacherModel, ScheduleModel.teacher_id == TeacherModel.id)
                .join(ClassroomModel, ScheduleModel.classroom_id == ClassroomModel.id)
                .join(BuildingModel, ClassroomModel.building_id == BuildingModel.id)
                .join(GroupModel, ScheduleModel.group_id == GroupModel.id)
                .outerjoin(inc_subquery, ScheduleModel.id == inc_subquery.c.event)
                .where(
                    and_(
                        ScheduleModel.timestamp_start <= func.current_timestamp(),
                        ScheduleModel.timestamp_end >= func.current_timestamp(),
                        or_(
                            # Статус 3 или 2, и прошло 5 минут
                            and_(
                                or_(
                                    inc_subquery.c.status == 3,
                                inc_subquery.c.status == 2
                            ),
                            func.current_timestamp() >= 
                                inc_subquery.c.time_created + text("INTERVAL '5 minutes'")
                                # inc_subquery.c.time_created + text("INTERVAL '1 minutes'")
                        ),
                        # Статус 0 и прошло 15 минут
                        and_(
                            inc_subquery.c.status == 0,
                            func.current_timestamp() >= 
                                inc_subquery.c.time_created + text("INTERVAL '15 minutes'")
                                # inc_subquery.c.time_created + text("INTERVAL '2 minutes'")
                        ),
                        # Или статус NULL
                        inc_subquery.c.status.is_(None)
                    )
                )
            )
            .order_by(
                desc('last_status_incident'),
                'time_created_incident'
            )
            .limit(1)
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
