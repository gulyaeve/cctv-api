from sqladmin import ModelView

from app.buildings.models import BuildingModel
from app.cameras.models import CameraModel
from app.classrooms.models import ClassroomModel
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
        ScheduleModel.duration,
    ]


class GroupsAdmin(ModelView, model=GroupModel):
    can_create = True
    can_delete = True
    name = "group"
    name_plural = "groups"
    column_list = [
        GroupModel.id,
        GroupModel.name,
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
        IncidentModel.classroom,
        IncidentModel.visor
    ]
# id = Column(Integer, primary_key=True, index=True)
#     comment = Column(String, nullable=False, index=True)
#     event: Mapped[int] = mapped_column(ForeignKey("schedules.id"))
#     time_created: Mapped[datetime] = mapped_column(server_default=func.now())
#     classroom_id: Mapped[int] = mapped_column(ForeignKey("classrooms.id"))
#     visor: Mapped[int] = mapped_column(ForeignKey("users.id"))
#
#     schedule: Mapped[List["ScheduleModel"]] = relationship(back_populates="incident")
#     classroom = relationship("ClassroomModel", back_populates="incident")
#     visor = relationship("UserModel", back_populates="incidents")

