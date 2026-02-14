from app.dao.base import BaseDAO
from app.groups.models import GroupModel


class GroupsDAO(BaseDAO):
    model = GroupModel

