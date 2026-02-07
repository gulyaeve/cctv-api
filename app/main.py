from fastapi import FastAPI
from sqladmin import Admin
from app.admin.views import UsersAdmin
from app.admin.auth import authentication_backend
from app.database import engine
from app.buildings.router import router as buildings_router
from app.classrooms.router import router as classrooms_router
from app.cameras.router import router as cameras_router
# from app.users.router import router as users_router



app = FastAPI(
    title="Система видеонаблюдения",
    version="0.1.0",
    root_path="/api"
)

app.include_router(buildings_router)
app.include_router(classrooms_router)
# app.include_router(users_router)
app.include_router(cameras_router)

admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)

