from app.dao.base import BaseDAO
from app.incidents.models import IncidentModel


class IncidentsDAO(BaseDAO):
    model = IncidentModel

