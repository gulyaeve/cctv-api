from app.dao.base import BaseDAO
from app.teachers.models import TeacherModel


class TeachersDAO(BaseDAO):
    model = TeacherModel

