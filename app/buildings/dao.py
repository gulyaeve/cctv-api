from app.buildings.models import Buildings
from app.dao.base import BaseDAO


class BuildingsDAO(BaseDAO):
    model = Buildings