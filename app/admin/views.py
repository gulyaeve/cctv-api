from sqladmin import ModelView

from app.buildings.models import BuildingModel
from app.cameras.models import CameraModel
from app.classrooms.models import ClassroomModel
from app.classrooms.type.models import ClassroomTypeModel
from app.incidents.answers.models import IncidentAnswerModel
from app.incidents.type.models import IncidentTypeModel
from app.users.models import UserModel
from app.users.models import Role
from app.users.models import Permission
from app.teachers.models import TeacherModel
from app.schedule.models import ScheduleModel
from app.groups.models import GroupModel
from app.incidents.models import IncidentModel


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
        UserModel.keycloak_uuid,
    ]
    form_excluded_columns = [UserModel.hashed_password]
    column_details_exclude_list = [UserModel.hashed_password]


class RolesAdmin(ModelView, model=Role):
    can_create = True
    can_delete = True
    name = "Роль"
    name_plural = "Роли"
    column_list = [
        Role.id,
        Role.name,
        Role.display_name,
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
        BuildingModel.number_of_floors,
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
        ClassroomModel.polygon_map,
        # ClassroomModel.cameras,
    ]


class ClassroomTypeAdmin(ModelView, model=ClassroomTypeModel):
    can_create = True
    can_delete = True
    name = "classroom type"
    name_plural = "classroom types"
    column_list = [
        ClassroomTypeModel.id,
        ClassroomTypeModel.name,
        ClassroomTypeModel.map_color,
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
        CameraModel.rtsp_url_preview,
        CameraModel.classroom,
        CameraModel.pos_x,
        CameraModel.pos_y,
        CameraModel.polygon_map,
        # CameraModel.camera_type,
    ]


class TeachersAdmin(ModelView, model=TeacherModel):
    can_create = True
    can_delete = True
    name = "teacher"
    name_plural = "teachers"
    column_list = [
        TeacherModel.id,
        TeacherModel.name,
    ]


class ScheduleAdmin(ModelView, model=ScheduleModel):
    can_create = True
    can_delete = True
    name = "schedule"
    name_plural = "schedules"
    column_list = [
        ScheduleModel.id,
        ScheduleModel.subject,
        ScheduleModel.classroom,
        ScheduleModel.teacher,
        ScheduleModel.timestamp_start,
        ScheduleModel.timestamp_end
    ]


class GroupsAdmin(ModelView, model=GroupModel):
    can_create = True
    can_delete = True
    name = "group"
    name_plural = "groups"
    column_list = [
        GroupModel.id,
        GroupModel.name,
        GroupModel.group_size,
    ]


class IncidentsAdmin(ModelView, model=IncidentModel):
    can_create = True
    can_delete = True
    name = "incident"
    name_plural = "incidents"
    column_list = [
        IncidentModel.id,
        IncidentModel.comment,
        IncidentModel.schedule,
        IncidentModel.visor,
    ]


class IncidentTypeAdmin(ModelView, model=IncidentTypeModel):
    can_create = True
    can_delete = True
    name = "incident type"
    name_plural = "incident types"
    column_list = [
        IncidentTypeModel.id,
        IncidentTypeModel.name,
        IncidentTypeModel.status_binding,
        IncidentTypeModel.event_type,
    ]

class IncidentAnswerAdmin(ModelView, model=IncidentAnswerModel):
    can_create = True
    can_delete = True
    name = "incident answer"
    name_plural = "incident answers"
    column_list = [
        IncidentAnswerModel.id,
        IncidentAnswerModel.author,
        IncidentAnswerModel.comment,
        IncidentAnswerModel.incident_id,
        IncidentAnswerModel.time_created,
    ]