from fastapi import APIRouter, FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin

from app.admin.views import (
    BuildingsAdmin,
    CamerasAdmin,
    ClassroomsAdmin,
    PermissionsAdmin,
    RolesAdmin,
    ScheduleAdmin,
    TeachersAdmin,
    UsersAdmin,
    GroupsAdmin,
)
from app.buildings.router import router as buildings_router
from app.cameras.router import router as cameras_router
from app.classrooms.router import router as classrooms_router
from app.teachers.router import router as teachers_router
from app.schedule.router import router as schedule_router

# from app.admin.auth import authentication_backend
from app.database import engine
from app.pages.router import router as pages_router
from app.users.router import router as users_router
from app.groups.router import router as groups_router

api = APIRouter(
    prefix="/api",
)
api.include_router(buildings_router)
api.include_router(classrooms_router)
api.include_router(users_router)
api.include_router(cameras_router)
api.include_router(teachers_router)
api.include_router(schedule_router)
api.include_router(groups_router)

app = FastAPI(title="Система видеонаблюдения", version="0.1.0")
app.mount("/static", StaticFiles(directory="app/static"), "static")
app.include_router(api)
app.include_router(pages_router)


# CORS
origins = [
    "http://127.0.0.1:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    # allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_methods=["*"],
    # allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", 
    #                "Access-Control-Allow-Origin", "Authorization"],
    allow_headers=["*"],
)


# admin = Admin(app, engine, authentication_backend=authentication_backend)
admin = Admin(app, engine)
admin.add_view(UsersAdmin)
admin.add_view(RolesAdmin)
admin.add_view(PermissionsAdmin)
admin.add_view(BuildingsAdmin)
admin.add_view(ClassroomsAdmin)
admin.add_view(CamerasAdmin)
admin.add_view(ScheduleAdmin)
admin.add_view(TeachersAdmin)
admin.add_view(GroupsAdmin)


@app.get("/", response_class=RedirectResponse)
def redirect_to_login_page():
    return RedirectResponse("/pages/login")
