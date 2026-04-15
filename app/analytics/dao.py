from app.logger import logger

from sqlalchemy.exc import SQLAlchemyError

from app.database import async_session_maker

from sqlalchemy import Date, and_, case, cast, func, select

from app.incidents.models import IncidentModel
from app.schedule.models import ScheduleModel


class AnalyticsDAO:
    @classmethod
    async def get_analytics(cls, **filter_by):      
        try:
            if filter_by.get("incident_status") is not None:
                incident_status = filter_by.get("incident_status")
                incidents_today = (
                    select(func.count())
                    .select_from(IncidentModel)
                    .filter(
                        and_(
                            cast(IncidentModel.time_created, Date) == func.current_date(),
                            IncidentModel.status == incident_status
                        )
                    )
                ).label("incidents_today")
                incidents_current_week = (
                    select(func.count(IncidentModel.id))
                    .where(
                        func.date_trunc('week', IncidentModel.time_created) == func.date_trunc('week', func.current_date()).cast(Date)
                    )
                    .filter(IncidentModel.status == incident_status)
                ).label("incidents_current_week")
                incidents_current_month = (
                    select(func.count(IncidentModel.id))
                    .where(
                        func.date_trunc('month', IncidentModel.time_created) == func.date_trunc('month', func.current_date()).cast(Date)
                    )
                    .filter(IncidentModel.status == incident_status)
                ).label("incidents_current_month")
            else:
                incidents_today = (
                    select(func.count())
                    .select_from(IncidentModel)
                    .filter(
                        cast(IncidentModel.time_created, Date) == func.current_date()
                    )
                ).label("incidents_today")
                incidents_current_week = (
                    select(func.count(IncidentModel.id))
                    .where(
                        func.date_trunc('week', IncidentModel.time_created) == func.date_trunc('week', func.current_date()).cast(Date)
                    )
                ).label("incidents_current_week")
                incidents_current_month = (
                    select(func.count(IncidentModel.id))
                    .where(
                        func.date_trunc('month', IncidentModel.time_created) == func.date_trunc('month', func.current_date()).cast(Date)
                    )
                ).label("incidents_current_month")

            if filter_by.get("schedule_status") is not None:
                schedule_status = filter_by.get("schedule_status")
                status_case = case(
                    (ScheduleModel.timestamp_start > func.current_timestamp(), 0),
                    (ScheduleModel.timestamp_end < func.current_timestamp(), 2),
                    else_=1
                ).label('status')
                schedules_today = (
                    select(func.count())
                    .select_from(ScheduleModel)
                    .filter(
                        and_(
                            cast(ScheduleModel.timestamp_start, Date) == func.current_date(),
                            status_case == schedule_status
                        )
                    )
                ).label("schedules_today")
                schedules_current_week = (
                    select(func.count(ScheduleModel.id))
                    .where(
                        func.date_trunc('week', ScheduleModel.timestamp_start) == func.date_trunc('week', func.current_date()).cast(Date)
                    )
                    .filter(status_case == schedule_status)
                ).label("schedules_current_week")
                schedules_current_month = (
                    select(func.count(ScheduleModel.id))
                    .where(
                        func.date_trunc('month', ScheduleModel.timestamp_start) == func.date_trunc('month', func.current_date()).cast(Date)
                    )
                    .filter(status_case == schedule_status)
                ).label("schedules_current_month")
            else:
                schedules_today = (
                    select(func.count())
                    .select_from(ScheduleModel)
                    .filter(cast(ScheduleModel.timestamp_start, Date) == func.current_date())
                ).label("schedules_today")
                schedules_current_week = (
                    select(func.count(ScheduleModel.id))
                    .where(
                        func.date_trunc('week', ScheduleModel.timestamp_start) == func.date_trunc('week', func.current_date()).cast(Date)
                    )
                ).label("schedules_current_week")
                schedules_current_month = (
                    select(func.count(ScheduleModel.id))
                    .where(
                        func.date_trunc('month', ScheduleModel.timestamp_start) == func.date_trunc('month', func.current_date()).cast(Date)
                    )
                ).label("schedules_current_month")

            query = select(
                incidents_today,
                incidents_current_week,
                incidents_current_month,
                schedules_today,
                schedules_current_week,
                schedules_current_month,
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