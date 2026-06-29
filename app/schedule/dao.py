from datetime import date
from typing import Optional

from sqlalchemy import Date, and_, asc, case, cast, desc, func, null, select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import aliased

from app.buildings.models import BuildingModel
from app.cameras.models import CameraModel
from app.classrooms.models import ClassroomModel
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.groups.models import GroupModel
from app.incidents.models import IncidentModel
from app.logger import logger
from app.schedule.models import ScheduleModel
from app.teachers.models import TeacherModel
from app.utils.filter_factory import filter_factory


class ScheduleDAO(BaseDAO):
    model = ScheduleModel

    @classmethod
    async def find_by_id(cls, id: int):
        try:
            status_case = case(
                (ScheduleModel.timestamp_start > func.current_timestamp(), 0),
                (ScheduleModel.timestamp_end < func.current_timestamp(), 2),
                else_=1,
            ).label("status")
            query = (
                select(
                    ScheduleModel.__table__,
                    TeacherModel.name.label("teacher_name"),
                    GroupModel.name.label("group_name"),
                    ClassroomModel.name.label("classroom_name"),
                    BuildingModel.id.label("building_id"),
                    BuildingModel.name.label("building_name"),
                    status_case,
                )
                .select_from(ScheduleModel)
                .join(ClassroomModel, ScheduleModel.classroom_id == ClassroomModel.id)
                .join(TeacherModel, ScheduleModel.teacher_id == TeacherModel.id)
                .join(GroupModel, ScheduleModel.group_id == GroupModel.id)
                .join(BuildingModel, ClassroomModel.building_id == BuildingModel.id)
                .filter(ScheduleModel.id == id)
                .order_by(ScheduleModel.id)
            )
            async with async_session_maker() as session:
                result = await session.execute(query)
                return result.mappings().one_or_none()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Data not found"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Data not found"

            logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            return None

    @classmethod
    async def find_all(cls, **filter_by):
        date_from = (
            filter_by.pop("date_from")
            if filter_by.get("date_from") is not None
            else None
        )
        date_to = (
            filter_by.pop("date_to") if filter_by.get("date_to") is not None else None
        )

        status = (
            filter_by.pop("status") if filter_by.get("status") is not None else None
        )

        filter_mapping = {
            "subject": ScheduleModel.subject,
            "classroom_id": ScheduleModel.classroom_id,
            "event_type": ScheduleModel.event_type,
            "building_id": BuildingModel.id,
            "teacher_id": ScheduleModel.teacher_id,
            "group_id": ScheduleModel.group_id,
        }
        conditions = filter_factory(filter_mapping, filter_by)

        if date_from is not None and date_to is not None:
            if date_from == date_to:
                filter_query = and_(
                    cast(ScheduleModel.timestamp_start, Date) == date_from, *conditions
                )
            else:
                filter_query = and_(
                    ScheduleModel.timestamp_start.between(date_from, date_to),
                    *conditions,
                )
        elif date_from is not None and date_to is None:
            filter_query = and_(
                cast(ScheduleModel.timestamp_start, Date) >= date_from, *conditions
            )
        elif date_from is None and date_to is not None:
            filter_query = and_(
                cast(ScheduleModel.timestamp_start, Date) <= date_to, *conditions
            )
        else:
            filter_query = and_(*conditions)

        try:
            status_case = case(
                (ScheduleModel.timestamp_start > func.current_timestamp(), 0),
                (ScheduleModel.timestamp_end < func.current_timestamp(), 2),
                else_=1,
            ).label("status")
            query = (
                select(
                    ScheduleModel.__table__,
                    TeacherModel.name.label("teacher_name"),
                    GroupModel.name.label("group_name"),
                    ClassroomModel.name.label("classroom_name"),
                    BuildingModel.id.label("building_id"),
                    BuildingModel.name.label("building_name"),
                    status_case,
                )
                .select_from(ScheduleModel)
                .join(ClassroomModel, ScheduleModel.classroom_id == ClassroomModel.id)
                .join(TeacherModel, ScheduleModel.teacher_id == TeacherModel.id)
                .join(GroupModel, ScheduleModel.group_id == GroupModel.id)
                .join(BuildingModel, ClassroomModel.building_id == BuildingModel.id)
                .filter(
                    filter_query
                    if status is None
                    else and_(status_case == status, filter_query)
                )
                .order_by(ScheduleModel.id)
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

    @classmethod
    async def find_all_count(cls, **filter_by):
        date_from = (
            filter_by.pop("date_from")
            if filter_by.get("date_from") is not None
            else None
        )
        date_to = (
            filter_by.pop("date_to") if filter_by.get("date_to") is not None else None
        )

        status = (
            filter_by.pop("status") if filter_by.get("status") is not None else None
        )

        filter_mapping = {
            "subject": ScheduleModel.subject,
            "classroom_id": ScheduleModel.classroom_id,
            "event_type": ScheduleModel.event_type,
            "building_id": BuildingModel.id,
            "teacher_id": ScheduleModel.teacher_id,
            "group_id": ScheduleModel.group_id,
        }
        conditions = filter_factory(filter_mapping, filter_by)

        if date_from is not None and date_to is not None:
            if date_from == date_to:
                filter_query = and_(
                    cast(ScheduleModel.timestamp_start, Date) == date_from, *conditions
                )
            else:
                filter_query = and_(
                    ScheduleModel.timestamp_start.between(date_from, date_to),
                    *conditions,
                )
        elif date_from is not None and date_to is None:
            filter_query = and_(
                cast(ScheduleModel.timestamp_start, Date) >= date_from, *conditions
            )
        elif date_from is None and date_to is not None:
            filter_query = and_(
                cast(ScheduleModel.timestamp_start, Date) <= date_to, *conditions
            )
        else:
            filter_query = and_(*conditions)

        try:
            status_case = case(
                (ScheduleModel.timestamp_start > func.current_timestamp(), 0),
                (ScheduleModel.timestamp_end < func.current_timestamp(), 2),
                else_=1,
            ).label("status")
            query = (
                select(
                    func.count(ScheduleModel.id),
                )
                .select_from(ScheduleModel)
                .join(ClassroomModel, ScheduleModel.classroom_id == ClassroomModel.id)
                .join(TeacherModel, ScheduleModel.teacher_id == TeacherModel.id)
                .join(GroupModel, ScheduleModel.group_id == GroupModel.id)
                .join(BuildingModel, ClassroomModel.building_id == BuildingModel.id)
                .filter(
                    filter_query
                    if status is None
                    else and_(status_case == status, filter_query)
                )
            )
            async with async_session_maker() as session:
                result = await session.execute(query)
                return result.scalar()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Data not found"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Data not found"

            logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            return None

    @classmethod
    async def find_by_date(cls, search_date: date, building_id: int):
        try:
            query = (
                select(
                    ScheduleModel.__table__,
                    CameraModel.id.label("camera_id"),
                    CameraModel.rtsp_url.label("camera_rtsp"),
                )
                .select_from(ScheduleModel)
                .join(
                    CameraModel, ScheduleModel.classroom_id == CameraModel.classroom_id
                )
                .join(ClassroomModel, ScheduleModel.classroom_id == ClassroomModel.id)
                .join(BuildingModel, ClassroomModel.building_id == BuildingModel.id)
                .filter(
                    and_(
                        cast(ScheduleModel.timestamp_start, Date) == search_date,
                        BuildingModel.id == building_id,
                    )
                )
                .order_by(ScheduleModel.id)
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

    @classmethod
    async def get_schedule_for_active_monitoring(
        cls,
        visor_id: int,
        building_id: Optional[int] = None,
        event_type: Optional[int] = None,
        classroom_id: Optional[int] = None,
        group_id: Optional[int] = None,
    ):
        try:
            # Алиас для инцидентов (для подзапроса)
            incident_subquery = (
                select(IncidentModel)
                .where(IncidentModel.visor_id == visor_id)
                .distinct(IncidentModel.event)
                .order_by(IncidentModel.event, IncidentModel.time_created.desc())
            ).subquery("inc")

            current_time = func.current_timestamp()

            conditions = [
                ScheduleModel.timestamp_start <= current_time,
                ScheduleModel.timestamp_end >= current_time,
            ]
            if building_id is not None:
                conditions.append(BuildingModel.id == building_id)
            if event_type is not None:
                conditions.append(ScheduleModel.event_type == event_type)
            if classroom_id is not None:
                conditions.append(ClassroomModel.id == classroom_id)
            if group_id is not None:
                conditions.append(GroupModel.id == group_id)

            # Incaliased = aliased(IncidentModel, incident_subquery)
            Curator = aliased(TeacherModel, name="curator")
            
            query = (
                select(
                    ScheduleModel.id.label("current_subject_id"),
                    ScheduleModel.subject.label("current_subject"),
                    ScheduleModel.timestamp_start,
                    ScheduleModel.timestamp_end,
                    TeacherModel.name.label("current_teacher"),
                    ClassroomModel.name.label("current_classroom"),
                    ClassroomModel.id.label("current_classroom_id"),
                    BuildingModel.name.label("current_building"),
                    BuildingModel.id.label("building_id"),
                    Curator.name.label("curator"),
                    GroupModel.name.label("current_group"),
                    GroupModel.group_size.label("group_size"),
                    func.coalesce(incident_subquery.c.status, 1).label(
                        "last_status_incident"
                    ),
                    incident_subquery.c.time_created.label("time_created_incident"),
                    # логика для cooldown
                    case(
                        (
                            and_(
                                incident_subquery.c.status.in_([2, 3]),
                                current_time
                                >= incident_subquery.c.time_created
                                + text("INTERVAL '3 minutes'"),
                            ),
                            1,
                        ),
                        (
                            and_(
                                incident_subquery.c.status == 0,
                                current_time
                                >= incident_subquery.c.time_created
                                + text("INTERVAL '6 minutes'"),
                            ),
                            1,
                        ),
                        (incident_subquery.c.status.is_(null()), 1),
                        else_=0,
                    ).label("cooldown"),
                )
                .select_from(ScheduleModel)
                .join(TeacherModel, ScheduleModel.teacher_id == TeacherModel.id)
                .join(ClassroomModel, ScheduleModel.classroom_id == ClassroomModel.id)
                .join(BuildingModel, ClassroomModel.building_id == BuildingModel.id)
                .join(GroupModel, ScheduleModel.group_id == GroupModel.id)
                .outerjoin(Curator, GroupModel.teacher_id == Curator.id)
                .outerjoin(
                    incident_subquery, ScheduleModel.id == incident_subquery.c.event
                )
                # Конструкция фильтрации по временам
                .where(and_(*conditions))
                # Заказ сортировки
                .order_by(
                    desc("cooldown"),
                    desc("last_status_incident"),
                    asc("time_created_incident"),
                )
                .limit(1)
            )

            # inc_subquery = (
            #     select(
            #         IncidentModel.event,
            #         IncidentModel.status,
            #         IncidentModel.time_created
            #     )
            #     .where(IncidentModel.visor_id == visor_id)
            #     .distinct(IncidentModel.event)
            #     .order_by(
            #         IncidentModel.event,
            #         desc(IncidentModel.time_created)
            #     )
            # ).subquery('inc')

            # # Основной запрос
            # query = (
            #     select(
            #         ScheduleModel.id.label('current_subject_id'),
            #         ScheduleModel.subject.label('current_subject'),
            #         ScheduleModel.timestamp_start,
            #         ScheduleModel.timestamp_end,
            #         TeacherModel.name.label('current_teacher'),
            #         ClassroomModel.name.label('current_classroom'),
            #         ClassroomModel.id.label('current_classroom_id'),
            #         BuildingModel.name.label('current_building'),
            #         GroupModel.name.label('current_group'),
            #         func.coalesce(inc_subquery.c.status, 1).label('last_status_incident'),
            #         inc_subquery.c.time_created.label('time_created_incident')
            #     )
            #     .select_from(ScheduleModel)
            #     .join(TeacherModel, ScheduleModel.teacher_id == TeacherModel.id)
            #     .join(ClassroomModel, ScheduleModel.classroom_id == ClassroomModel.id)
            #     .join(BuildingModel, ClassroomModel.building_id == BuildingModel.id)
            #     .join(GroupModel, ScheduleModel.group_id == GroupModel.id)
            #     .outerjoin(inc_subquery, ScheduleModel.id == inc_subquery.c.event)
            #     .where(
            #         and_(
            #             ScheduleModel.timestamp_start <= func.current_timestamp(),
            #             ScheduleModel.timestamp_end >= func.current_timestamp(),
            #             or_(
            #                 # Статус 3 или 2, и прошло 5 минут
            #                 and_(
            #                     or_(
            #                         inc_subquery.c.status == 3,
            #                     inc_subquery.c.status == 2
            #                 ),
            #                 func.current_timestamp() >=
            #                     # inc_subquery.c.time_created + text("INTERVAL '5 minutes'")
            #                     inc_subquery.c.time_created + text("INTERVAL '3 minutes'")
            #             ),
            #             # Статус 0 и прошло 15 минут
            #             and_(
            #                 inc_subquery.c.status == 0,
            #                 func.current_timestamp() >=
            #                     # inc_subquery.c.time_created + text("INTERVAL '15 minutes'")
            #                     inc_subquery.c.time_created + text("INTERVAL '6 minutes'")
            #             ),
            #             # Или статус NULL
            #             inc_subquery.c.status.is_(None)
            #         )
            #     )
            # )
            # .order_by(
            #     desc('last_status_incident'),
            #     'time_created_incident'
            # )
            # .limit(1)
            # )

            async with async_session_maker() as session:
                result = await session.execute(query)
                return result.mappings().one_or_none()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Data not found"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Data not found"

            logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            return None
