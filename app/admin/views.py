from sqladmin import ModelView

from app.buildings.models import BuildingModel
from app.cameras.models import CameraModel
from app.classrooms.models import ClassroomModel
from app.users.models import UserModel
from app.users.models import Role
from app.users.models import Permission


class UsersAdmin(ModelView, model=UserModel):
    can_create = False
    can_delete = True
    name = "Пользователь"
    name_plural = "Пользователи"
    column_list = [
        UserModel.id,
        UserModel.username,
        UserModel.full_name,
        UserModel.email,
        # UserModel.phone,
        UserModel.time_created,
        UserModel.last_login,
        UserModel.roles,
    ]
    column_details_exclude_list = [UserModel.hashed_password]


class RolesAdmin(ModelView, model=Role):
    can_create = True
    can_delete = True
    name = "Роль"
    name_plural = "Роли"
    column_list = [
        Role.id,
        Role.name,
    ]


class PermissionsAdmin(ModelView, model=Permission):
    can_create = True
    can_delete = True
    name = "Доступ"
    name_plural = "Доступы"
    column_list = [
        Permission.id,
        Permission.name,
    ]


class BuildingsAdmin(ModelView, model=BuildingModel):
    can_create = True
    can_delete = True
    name = "building"
    name_plural = "buildings"
    column_list = [
        BuildingModel.id,
        BuildingModel.name,
        # BuildingModel.classrooms,
        BuildingModel.location,
    ]


class ClassroomsAdmin(ModelView, model=ClassroomModel):
    can_create = True
    can_delete = True
    name = "classroom"
    name_plural = "classrooms"
    column_list = [
        ClassroomModel.id,
        ClassroomModel.name,
        ClassroomModel.floor,
        ClassroomModel.building,
        # ClassroomModel.cameras,
    ]


class CamerasAdmin(ModelView, model=CameraModel):
    can_create = True
    can_delete = True
    name = "camera"
    name_plural = "cameras"
    column_list = [
        CameraModel.id,
        CameraModel.view,
        CameraModel.camera_ip,
        CameraModel.reg_ip,
        CameraModel.rtsp_url,
        CameraModel.classroom,
    ]
