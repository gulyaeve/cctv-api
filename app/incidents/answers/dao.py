from app.dao.base import BaseDAO
from app.incidents.answers.models import IncidentAnswerModel


class IncidentAnswerDAO(BaseDAO):
    model = IncidentAnswerModel