from app.incidents.answers.models import IncidentAnswerModel
from app.incidents.schemas import IncidentAppendScheme
from app.incidents.type.models import IncidentTypeModel
from app.logger import logger
from sqlalchemy import ARRAY, Date, String, and_, cast, desc, distinct, func, select
from sqlalchemy.dialects.postgresql import JSONB
from app.buildings.models import BuildingModel
from app.database import async_session_maker
from app.classrooms.models import ClassroomModel
from app.dao.base import BaseDAO
from app.groups.models import GroupModel
from app.incidents.models import IncidentModel
from app.schedule.models import ScheduleModel
from app.teachers.models import TeacherModel
from app.users.models import UserModel
from sqlalchemy.exc import SQLAlchemyError

from app.utils.filter_factory import filter_factory


class IncidentsDAO(BaseDAO):
    model = IncidentModel

    @classmethod
    async def add(cls, data: IncidentAppendScheme):
        try:
            async with async_session_maker() as session:
                if data.incident_types:
                    incident_types_query = await session.execute(
                        select(IncidentTypeModel).where(IncidentTypeModel.id.in_(data.incident_types))
                    )
                    incident_types = incident_types_query.scalars().all()
                    data_to_save = data.model_dump(exclude={"building_id", "incident_types"})
                    new_incident: IncidentModel = IncidentModel(**data_to_save)
                    new_incident.incident_types = list(incident_types)
                else:
                    data_to_save = data.model_dump(exclude={"building_id", "incident_types"})
                    new_incident: IncidentModel = IncidentModel(**data_to_save)
                session.add(new_incident)
                await session.commit()
                await session.refresh(new_incident)
                return new_incident
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot insert data into table"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot insert data into table"

            logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            return None

    @classmethod
    async def find_all(cls, **filter_by):
        date_from = filter_by.pop("date_from") if filter_by.get("date_from") else None
        date_to = filter_by.pop("date_to") if filter_by.get("date_to") else None

        filter_mapping = {
            "comment": IncidentModel.comment,
            "event": IncidentModel.event,
            "visor_id": IncidentModel.visor_id,
            "status": IncidentModel.status,
            "classroom_id": ClassroomModel.id,
            "building_id": BuildingModel.id,
            "teacher_id": TeacherModel.id,
            "subject": ScheduleModel.subject,
            "teacher_name": TeacherModel.name,
            "incident_type_id": IncidentTypeModel.id,
        }
        conditions = filter_factory(filter_mapping, filter_by)

        if date_from is not None and date_to is not None:
            if date_from == date_to:
                filter_query = and_(cast(IncidentModel.time_created, Date) == date_from, *conditions)
            else:
                filter_query = and_(IncidentModel.time_created.between(date_from, date_to), *conditions)
        elif date_from is not None and date_to is None:
            filter_query = and_(cast(IncidentModel.time_created, Date) >= date_from, *conditions)
        elif date_from is None and date_to is not None:
            filter_query = and_(cast(IncidentModel.time_created, Date) <= date_to, *conditions)
        else:
            filter_query = and_(*conditions)

        try:           
            # answers_agg_subquery = (
            #     select(
            #         IncidentAnswerModel.incident_id,
            #         func.jsonb_agg(IncidentAnswerModel.__table__.table_valued()).label("answers_list")
            #     )
            #     .group_by(IncidentAnswerModel.incident_id)
            #     .subquery()
            # )

            query = (
                select(
                    IncidentModel.__table__,
                    ClassroomModel.id.label("classroom_id"),
                    ClassroomModel.name.label("classroom_name"),
                    BuildingModel.id.label("building_id"),
                    BuildingModel.name.label("building_name"),
                    UserModel.full_name.label("visor_name"),
                    ScheduleModel.teacher_id.label("teacher_id"),
                    ScheduleModel.subject.label("subject"),
                    TeacherModel.name.label("teacher_name"),
                    func.coalesce(
                        func.array_agg(distinct(IncidentTypeModel.name)).filter(IncidentTypeModel.name.is_not(None)),
                        func.cast([], ARRAY(String))
                    ).label('incident_type_names'),
                    # func.coalesce(answers_agg_subquery.c.answers_list, func.cast([], JSONB)).label("incident_answers")
                )
                .join(ScheduleModel, IncidentModel.event == ScheduleModel.id)
                .join(TeacherModel, ScheduleModel.teacher_id == TeacherModel.id)
                .join(ClassroomModel, ScheduleModel.classroom_id == ClassroomModel.id)
                .join(BuildingModel, ClassroomModel.building_id == BuildingModel.id)
                .join(UserModel, IncidentModel.visor_id == UserModel.id)
                .outerjoin(IncidentModel.incident_types)
                # .outerjoin(answers_agg_subquery, IncidentModel.id == answers_agg_subquery.c.incident_id) 
                .filter(filter_query)
                .order_by(desc(IncidentModel.time_created))
                .group_by(
                    IncidentModel,
                    TeacherModel.name,
                    ScheduleModel.subject,
                    ScheduleModel.teacher_id,
                    ClassroomModel.id,
                    ClassroomModel.name,
                    UserModel.full_name,
                    BuildingModel.id,
                    BuildingModel.name,
                    # answers_agg_subquery.c.answers_list
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
        
    @classmethod
    async def find_all_count(cls, **filter_by):
        date_from = filter_by.pop("date_from") if filter_by.get("date_from") else None
        date_to = filter_by.pop("date_to") if filter_by.get("date_to") else None

        filter_mapping = {
            "comment": IncidentModel.comment,
            "event": IncidentModel.event,
            "visor_id": IncidentModel.visor_id,
            "status": IncidentModel.status,
            "classroom_id": ClassroomModel.id,
            "building_id": BuildingModel.id,
            "teacher_id": TeacherModel.id,
            "subject": ScheduleModel.subject,
            "teacher_name": TeacherModel.name,
        }
        conditions = filter_factory(filter_mapping, filter_by)

        if date_from is not None and date_to is not None:
            if date_from == date_to:
                filter_query = and_(cast(IncidentModel.time_created, Date) == date_from, *conditions)
            else:
                filter_query = and_(IncidentModel.time_created.between(date_from, date_to), *conditions)
        elif date_from is not None and date_to is None:
            filter_query = and_(cast(IncidentModel.time_created, Date) >= date_from, *conditions)
        elif date_from is None and date_to is not None:
            filter_query = and_(cast(IncidentModel.time_created, Date) <= date_to, *conditions)
        else:
            filter_query = and_(*conditions)

        try:
            query = (
                select(
                    func.count(IncidentModel.id),
                )
                .select_from(IncidentModel)
                .join(ScheduleModel, IncidentModel.event == ScheduleModel.id)
                .join(TeacherModel, ScheduleModel.teacher_id == TeacherModel.id)
                .join(ClassroomModel, ScheduleModel.classroom_id == ClassroomModel.id)
                .join(BuildingModel, ClassroomModel.building_id == BuildingModel.id)
                .filter(filter_query)
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
    async def get_incidents_info(cls, visor_id: int, event_id: int):
        try:
            query = (
                select(
                    IncidentModel.__table__,
                    TeacherModel.name.label('current_teacher'),
                    GroupModel.name.label('current_group'),
                    ScheduleModel.subject.label('current_schedule'),
                    BuildingModel.id.label('building_id'),
                    ClassroomModel.name.label('current_classroom'),
                    UserModel.full_name.label('current_visor')
                )
                .join(ScheduleModel, IncidentModel.event == ScheduleModel.id)
                .join(ClassroomModel, ScheduleModel.classroom_id == ClassroomModel.id)
                .join(BuildingModel, ClassroomModel.building_id == BuildingModel.id)
                .join(TeacherModel, ScheduleModel.teacher_id == TeacherModel.id)
                .join(GroupModel, ScheduleModel.group_id == GroupModel.id)
                .join(UserModel, IncidentModel.visor_id == UserModel.id)
                .filter(IncidentModel.visor_id == visor_id, IncidentModel.event == event_id)
                .order_by(desc(IncidentModel.time_created))
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
    async def get_incident_full_info(cls, id: int):
        try:
            answers_agg_subquery = (
                select(
                    IncidentAnswerModel.incident_id,
                    func.jsonb_agg(IncidentAnswerModel.__table__.table_valued()).label("answers_list")
                )
                .group_by(IncidentAnswerModel.incident_id)
                .subquery()
            )

            query = (
                select(
                    IncidentModel.__table__,
                    TeacherModel.name.label('current_teacher'),
                    GroupModel.name.label('current_group'),
                    ScheduleModel.subject.label('current_schedule'),
                    ClassroomModel.id.label('classroom_id'),
                    ClassroomModel.name.label('current_classroom'),
                    UserModel.full_name.label('current_visor'),
                    BuildingModel.id.label('building_id'),
                    BuildingModel.name.label('current_building'),
                    func.coalesce(
                        func.array_agg(IncidentTypeModel.name).filter(IncidentTypeModel.name.is_not(None)),
                        func.cast([], ARRAY(String))
                    ).label('incident_type_names'),
                    func.coalesce(answers_agg_subquery.c.answers_list, func.cast([], JSONB)).label("incident_answers")
                )
                .join(ScheduleModel, IncidentModel.event == ScheduleModel.id)
                .join(ClassroomModel, ScheduleModel.classroom_id == ClassroomModel.id)
                .join(TeacherModel, ScheduleModel.teacher_id == TeacherModel.id)
                .join(GroupModel, ScheduleModel.group_id == GroupModel.id)
                .join(UserModel, IncidentModel.visor_id == UserModel.id)
                .join(BuildingModel, ClassroomModel.building_id == BuildingModel.id)
                .outerjoin(IncidentModel.incident_types)
                .outerjoin(answers_agg_subquery, IncidentModel.id == answers_agg_subquery.c.incident_id) 
                .filter(IncidentModel.id == id)
                .group_by(
                    IncidentModel.id,
                    TeacherModel.name,
                    GroupModel.name,
                    ScheduleModel.subject,
                    ClassroomModel.id,
                    ClassroomModel.name,
                    UserModel.full_name,
                    BuildingModel.id,
                    BuildingModel.name,
                    answers_agg_subquery.c.answers_list
                )
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
