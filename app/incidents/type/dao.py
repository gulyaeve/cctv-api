from app.dao.base import BaseDAO
from app.incidents.type.models import IncidentTypeModel


class IncidentTypeDAO(BaseDAO):
    model = IncidentTypeModel