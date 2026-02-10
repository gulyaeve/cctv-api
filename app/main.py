from fastapi import APIRouter, FastAPI
from sqladmin import Admin

from app.admin.views import (
    BuildingsAdmin,
    CamerasAdmin,
    ClassroomsAdmin,
    PermissionsAdmin,
    RolesAdmin,
    UsersAdmin,
)
from app.buildings.router import router as buildings_router
from app.cameras.router import router as cameras_router
from app.classrooms.router import router as classrooms_router

# from app.admin.auth import authentication_backend
from app.database import engine
from app.pages.router import router as pages_router
from app.users.router import router as users_router

api = APIRouter(
    prefix="/api",
)
api.include_router(buildings_router)
api.include_router(classrooms_router)
api.include_router(users_router)
api.include_router(cameras_router)

app = FastAPI(title="Система видеонаблюдения", version="0.1.0")
app.include_router(api)
app.include_router(pages_router)

# admin = Admin(app, engine, authentication_backend=authentication_backend)
admin = Admin(app, engine)
admin.add_view(UsersAdmin)
admin.add_view(RolesAdmin)
admin.add_view(PermissionsAdmin)
admin.add_view(BuildingsAdmin)
admin.add_view(ClassroomsAdmin)
admin.add_view(CamerasAdmin)
