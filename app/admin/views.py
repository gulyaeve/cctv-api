from sqladmin import ModelView

from app.buildings.models import BuildingModel
from app.cameras.models import CameraModel
from app.classrooms.models import ClassroomModel

# from app.users.models import UserModel


# class UsersAdmin(ModelView, model=UserModel):
#     can_create = False
#     can_delete = True
#     name = "Пользователь"
#     name_plural = "Пользователи"
#     column_list = [
#         UserModel.id,
#         UserModel.name,
#         UserModel.surname,
#         UserModel.patronymic,
#         UserModel.email,
#         UserModel.phone,
#     ]
#     column_details_exclude_list = [UserModel.hashed_password]

class BuildingsAdmin(ModelView, model=BuildingModel):
    can_create = False
    can_delete = True
    # name = "building"
    # name_plural = "buildings"


class ClassroomsAdmin(ModelView, model=ClassroomModel):
    can_create = False
    can_delete = True
    # name = "classroom"
    # name_plural = "classrooms"


class CamerasAdmin(ModelView, model=CameraModel):
    can_create = False
    can_delete = True
    # name = "camera"
    # name_plural = "cameras"
