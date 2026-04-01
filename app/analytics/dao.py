import logging
from typing import Literal, Optional

from sqlalchemy.exc import SQLAlchemyError

from app.database import async_session_maker

from sqlalchemy import Date, cast, func, select

from app.incidents.models import IncidentModel
from app.schedule.models import ScheduleModel


class AnalyticsDAO:
    @classmethod
    async def get_analytics(cls):
        try:
            incidents_today = (
                select(func.count())
                .select_from(IncidentModel)
                .filter(cast(IncidentModel.time_created, Date) == func.current_date())
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

            logging.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            return None