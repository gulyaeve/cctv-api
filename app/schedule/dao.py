from app.schedule.models import ScheduleModel
from app.dao.base import BaseDAO


class ScheduleDAO(BaseDAO):
    model = ScheduleModel