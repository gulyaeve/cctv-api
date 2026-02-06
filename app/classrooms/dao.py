from app.classrooms.models import ClassroomModel
from app.dao.base import BaseDAO


class ClassroomsDAO(BaseDAO):
    model = ClassroomModel