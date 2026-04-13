from app.classrooms.type.models import ClassroomTypeModel
from app.dao.base import BaseDAO


class ClassroomTypeDAO(BaseDAO):
    model = ClassroomTypeModel