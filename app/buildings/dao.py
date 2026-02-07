from app.buildings.models import BuildingModel
from app.dao.base import BaseDAO


class BuildingsDAO(BaseDAO):
    model = BuildingModel
